import os
import tempfile
import shutil
import cadquery as cq
from django.conf import settings

def export_tile(tile, config, version="v2.0", cache_results=False):
    """
    Exports the tile to STEP and STL files using the YAML-defined file name.
    """
    export_formats = config.get("export_formats", ["step", "stl"])
    tile_type = config.get("tile_type", "bricks")  # Defaults to bricks if not specified
    file_name = config.get("file_name", f"{tile_type}_tile")  # Uses default if not in YAML

    output_dir = os.path.join(settings.MEDIA_ROOT, "cad_pipeline", "tiles", tile_type, f"v{version}")
    os.makedirs(output_dir, exist_ok=True)

    cache = {}

    for fmt in export_formats:
        file_path = os.path.join(output_dir, f"{file_name}_{version}.{fmt}")  # 👈 Uses YAML file name

        try:
            if fmt == "step":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".step") as tmp_file:
                    step_temp_path = tmp_file.name
                cq.exporters.export(tile.toCompound(), step_temp_path)
                shutil.move(step_temp_path, file_path)

            elif fmt == "stl":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmp_file:
                    stl_temp_path = tmp_file.name
                cq.exporters.export(tile.toCompound(), stl_temp_path)
                shutil.move(stl_temp_path, file_path)

            else:
                raise ValueError(f"Unsupported export format: {fmt}")

            print(f"✅ {fmt.upper()} file exported to: {file_path}")

            if cache_results:
                with open(file_path, "rb") as f:
                    cache[fmt] = f.read()

        except Exception as e:
            raise RuntimeError(f"❌ Export failed for format {fmt}: {e}")

    return cache if cache_results else None
