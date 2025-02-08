import tempfile
import shutil
import cadquery as cq
from django.core.cache import cache

def export_assembly_cached(assembly, config):
    """
    Generic function to cache and export any assembly type (brick, tile, wall, etc.).
    """
    export_formats = config.get("export_formats", ["step", "stl"])
    tile_type = assembly.model_type  # Uses the assembly's model type
    file_name = config.get("file_name", f"{tile_type}_export")  

    cache_key = f"assembly_export:{assembly.id}"
    cached_files = cache.get(cache_key)

    if cached_files:
        return cached_files  # ✅ Return cached export if available

    cache_files = {}

    for fmt in export_formats:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{fmt}") as tmp_file:
                temp_path = tmp_file.name
            cq.exporters.export(assembly.toCompound(), temp_path)

            with open(temp_path, "rb") as f:
                cache_files[fmt] = f.read()

        except Exception as e:
            raise RuntimeError(f"❌ Export failed for format {fmt}: {e}")

    cache.set(cache_key, cache_files, timeout=86400)  # ✅ Cache export for fast access
    return cache_files
