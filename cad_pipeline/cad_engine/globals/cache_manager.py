import tempfile
import cadquery as cq
from django.core.cache import cache
from cad_pipeline.models.exported_file import ExportedFile


def cache_model(model, cache_key, export_format="step"):
    """
    Serializes and caches a CadQuery model as a STEP or STL file.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{export_format}") as tmp_file:
            temp_path = tmp_file.name

        # ✅ Export model in the correct format
        cq.exporters.export(model, temp_path, export_format.upper())

        # ✅ Read the file and cache the binary data
        with open(temp_path, "rb") as file:
            cache.set(cache_key, file.read(), timeout=86400)

        print(f"✅ Cached Model: {cache_key} ({export_format.upper()})")

    except Exception as e:
        raise RuntimeError(f"❌ Failed to cache model: {e}")


def retrieve_cached_model(cache_key):
    """
    Retrieves a cached STEP/STL file and reimports it into CadQuery.
    """
    cached_data = cache.get(cache_key)
    if cached_data:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".step") as tmp_file:
                tmp_file.write(cached_data)
                tmp_file_path = tmp_file.name
            return cq.importers.importStep(tmp_file_path)
        except Exception:
            print("\n⚠️ Warning: Cache deserialization failed. Recomputing...")
            return None
    return None


def is_cached(cache_key):
    """
    Checks if a model is cached.
    """
    return cache.get(cache_key) is not None


def clear_cache(cache_key):
    """
    Clears a specific model cache.
    """
    cache.delete(cache_key)
    print(f"✅ Cache cleared for: {cache_key}")


def cache_exported_file(exported_file):
    """
    Caches the exported file for quick retrieval.
    """
    cache_key = f"exported_file_{exported_file.id}"
    cache.set(cache_key, exported_file.file_data, timeout=86400)
    print(f"✅ Cached Exported File: {exported_file.file_name}")
