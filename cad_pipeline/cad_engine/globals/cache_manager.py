import logging
import tempfile
import cadquery as cq
from django.core.cache import cache
from cad_pipeline.models.exported_file import ExportedFile

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

### ✅ MODEL CACHING ###
def cache_model(model, cache_key, export_format="step"):
    """
    Serializes and caches a CadQuery model as a STEP or STL file.

    :param model: CadQuery Workplane model to cache.
    :param cache_key: Unique key for retrieving the cached model.
    :param export_format: Format for caching (default: "step").
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{export_format}") as tmp_file:
            temp_path = tmp_file.name

        # ✅ Export model in the correct format
        cq.exporters.export(model, temp_path, export_format.upper())

        # ✅ Read the file and cache the binary data
        with open(temp_path, "rb") as file:
            cache.set(cache_key, file.read(), timeout=86400)  # Cache for 1 day

        logging.info(f"✅ Cached Model: {cache_key} ({export_format.upper()})")

    except Exception as e:
        logging.error(f"❌ Failed to cache model: {e}")
        raise RuntimeError(f"Failed to cache model: {e}")

def retrieve_cached_model(cache_key):
    """
    Retrieves a cached STEP/STL file and reimports it into CadQuery.

    :param cache_key: Unique key for retrieving the cached model.
    :return: CadQuery Workplane model or None if cache is invalid.
    """
    cached_data = cache.get(cache_key)
    if cached_data:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".step") as tmp_file:
                tmp_file.write(cached_data)
                tmp_file_path = tmp_file.name
            return cq.importers.importStep(tmp_file_path)
        except Exception:
            logging.warning("⚠️ Cache deserialization failed. Recomputing model...")
            return None
    return None

def is_cached(cache_key):
    """
    Checks if a model is cached.

    :param cache_key: Unique key for the cached model.
    :return: Boolean indicating if the model is in the cache.
    """
    return cache.get(cache_key) is not None

def clear_cache(cache_key):
    """
    Clears a specific model cache.

    :param cache_key: Unique key for the cached model to be cleared.
    """
    cache.delete(cache_key)
    logging.info(f"✅ Cache cleared for: {cache_key}")


### ✅ EXPORT CACHING ###
def cache_exported_file(exported_file):
    """
    Caches the exported file for quick retrieval.

    :param exported_file: The exported file object from the database.
    """
    cache_key = f"exported_file_{exported_file.id}"
    cache.set(cache_key, exported_file.file_data, timeout=86400)
    logging.info(f"✅ Cached Exported File: {exported_file.file_name}")

def retrieve_cached_export(export_id):
    """
    Retrieves a cached exported file.

    :param export_id: The ID of the exported file in the database.
    :return: Cached file data or None if not found.
    """
    cache_key = f"exported_file_{export_id}"
    return cache.get(cache_key)

def clear_export_cache(export_id):
    """
    Clears a specific exported file cache.

    :param export_id: The ID of the exported file.
    """
    cache_key = f"exported_file_{export_id}"
    cache.delete(cache_key)
    logging.info(f"✅ Cache cleared for exported file ID: {export_id}")
