"""
Script: flemish_brick.py
Description: Generates a Flemish bond brick tile using modular helper functions.
Dependencies: CadQuery, Django settings, OCP CAD Viewer, PyYAML
"""

import os
import sys
import django
import cadquery as cq
from ocp_vscode import show_object  # Visualization for VS Code

# Add project root to sys.path for modular imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(project_root)

# Ensure resources package is recognized
from resources.configs.yaml_config import load_config, validate_config, get_default_config_path
from resources.helpers.file_helper import export_tile
from resources.helpers.brick_geometry import create_full_brick, create_half_brick

from django.conf import settings

# Ensure Django settings are properly configured
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railworks_project.settings")
django.setup()

# Load and validate configuration
tile_type = "bricks"
config_path = get_default_config_path(tile_type)
config = load_config(config_path)
validate_config(config, tile_type)


def create_flemish_tile():
    """
    Creates a Flemish bond tile with alternating row patterns.
    Even rows are offset so the centres of half bricks align with full bricks in odd rows.
    """
    tile_assembly = cq.Assembly()

    row_repetition = config["row_repetition"]
    tile_width = config["tile_width"]
    offset_X = config.get("offset_X", 0)

    for i in range(row_repetition):
        row_assembly = cq.Assembly()
        half_brick = create_half_brick(config)
        full_brick = create_full_brick(config)

        # Determine row offset for Flemish bond pattern
        row_x_offset = 0
        if i % 2 != 0:  # Offset even rows to maintain alignment
            row_x_offset = -config["brick_length"] / 1.5

        # Initialize X position
        x_offset = row_x_offset

        for j in range(tile_width):
            if j % 2 == 0:
                row_assembly.add(
                    full_brick,
                    loc=cq.Location(cq.Vector(x_offset, 0, 0)),
                    name=f"Full Brick Row{i}-Col{j}"
                )
                x_offset += config["brick_length"]
            else:
                row_assembly.add(
                    half_brick,
                    loc=cq.Location(cq.Vector(x_offset, 0, 0)),
                    name=f"Half Brick Row{i}-Col{j}"
                )
                x_offset += config["brick_length"] / 2

        # Set correct vertical stacking
        z_offset = i * config["brick_height"]
        tile_assembly.add(
            row_assembly,
            loc=cq.Location(cq.Vector(offset_X * i, 0, z_offset)),
            name=f"Row {i}"
        )

    return tile_assembly


# Main execution
if __name__ == "__main__":
    tile = create_flemish_tile()
    show_object(tile, name="Flemish Bond Tile")  # Visualize the tile
    export_tile(tile, version="v2.0", tile_type="bricks", export_formats=config["export_formats"])
