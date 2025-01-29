import os
from cadquery import exporters
from django.conf import settings

def export_tile(tile, version, tile_type, export_formats):
    """
    Exports the tile to the specified formats.
    :param tile: CadQuery Assembly object.
    :param version: Version string.
    :param tile_type: Type of tile (e.g., "bricks").
    :param export_formats: List of export formats.
    """
    output_dir = os.path.join(settings.MEDIA_ROOT, "resources", "tiles", tile_type, f"v{version}")
    os.makedirs(output_dir, exist_ok=True)

    for fmt in export_formats:
        file_path = os.path.join(output_dir, f"{tile_type}_tile_{version}.{fmt}")
        try:
            if fmt == "step":
                exporters.export(tile.toCompound(), file_path)
            elif fmt == "stl":
                exporters.export(tile.toCompound(), file_path)
            else:
                raise ValueError(f"Unsupported export format: {fmt}")
            print(f"{fmt.upper()} file exported to: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Export failed for format {fmt}: {e}")
