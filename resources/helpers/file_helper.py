"""
file_helpers.py - Handles exporting tile files in STL & STEP formats.
"""

import os
from cadquery import exporters
from django.conf import settings


def export_tile(tile, version: str, tile_type: str, export_formats: list):
    """
    Exports the tile to specified formats in a versioned directory.
    :param tile: The CADQuery object to export.
    :param version: Version identifier (e.g., "v2.0").
    :param tile_type: Type of tile (e.g., "bricks", "plain_track").
    :param export_formats: List of formats to export (["step", "stl"]).
    """
    output_dir = os.path.join(settings.MEDIA_ROOT, f"resources/tiles/{tile_type}/v{version}")
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
