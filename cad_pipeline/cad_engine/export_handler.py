import tempfile
import cadquery as cq
from django.core.cache import cache
from django.core.files.base import ContentFile

def export_assembly_cached(assembly, config):
    """
    Exports a CadQuery Workplane and caches the result.
    Now fully supports Workplane objects directly.
    """
    export_formats = config.get("export_formats", ["step", "stl"])
    file_name = config.get("file_name", "cached_tile")  # ✅ No longer depends on `.model_type`

    cache_key = f"assembly_export:{file_name.replace(' ', '_')}"  # ✅ Fix memcached error
    cached_files = cache.get(cache_key)

    if cached_files:
        return cached_files  # ✅ Return cached export if available

    cache_files = {}

    for fmt in export_formats:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{fmt}") as tmp_file:
                temp_path = tmp_file.name
            
            # ✅ Fix: Ensure Workplane objects are exported correctly
            if isinstance(assembly, cq.Workplane):
                cq.exporters.export(assembly, temp_path)
            else:
                raise TypeError(f"❌ Invalid object type: {type(assembly)}. Expected `Workplane`.")

            with open(temp_path, "rb") as f:
                cache_files[fmt] = f.read()

        except Exception as e:
            raise RuntimeError(f"❌ Export failed for format {fmt}: {e}")

    cache.set(cache_key, cache_files, timeout=86400)  # ✅ Cache export for fast access
    return cache_files
