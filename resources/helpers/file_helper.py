import os
from django.conf import settings

def export_tile(tile, version="v2.0", tile_type="brick_tile", export_formats=None):
    """
    Exports the tile to specified formats in a versioned directory.
    """
    if export_formats is None:
        export_formats = ["step", "stl"]

    output_dir = os.path.join(settings.MEDIA_ROOT, "resources", "tiles", tile_type, f"v{version}")

    # ✅ **Ensure `MEDIA_ROOT` exists**
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for fmt in export_formats:
        file_path = os.path.join(output_dir, f"{tile_type}_{version}.{fmt}")
        try:
            if fmt == "step":
                from cadquery import exporters
                exporters.export(tile.toCompound(), file_path)
            elif fmt == "stl":
                from cadquery import exporters
                exporters.export(tile.toCompound(), file_path)
            else:
                raise ValueError(f"Unsupported export format: {fmt}")
            print(f"✅ {fmt.upper()} file exported to: {file_path}")
        except Exception as e:
            raise RuntimeError(f"❌ Export failed for format {fmt}: {e}")
