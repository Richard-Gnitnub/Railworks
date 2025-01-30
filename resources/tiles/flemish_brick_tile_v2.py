"""
Script: flemish_brick_tile_v2.py
Description: Enhanced Flemish bond tile script with modular configuration and reusable row generation.
Dependencies: CadQuery, Django settings, OCP CAD Viewer, PyYAML
"""

import os
import sys
import django
import cadquery as cq
from cadquery import exporters
from ocp_vscode import show_object  # Enable visualization in VS Code

# Add the project root (where manage.py is located) to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

# Import configuration and tile generation functions
from resources.helpers.file_export import export_tile 
from resources.configs.yaml_config import load_config, validate_config
from resources.helpers.brick_geometry import create_full_brick_aligned, create_half_brick_aligned
from django.conf import settings

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railworks_project.settings")
django.setup()

# Load and validate configuration
config_path = os.path.join(project_root, "resources/configs/default_config_v2.yaml")
config = load_config(config_path)
validate_config(config)

# Validate tile configuration values
def validate_tile_parameters():
    """Validates the YAML configuration for tile dimensions and repetition settings."""
    if config["row_repetition"] <= 0:
        raise ValueError("Row repetition must be greater than 0.")
    if config["brick_length"] <= 0 or config["brick_width"] <= 0 or config["brick_height"] <= 0:
        raise ValueError("Brick dimensions must be greater than 0.")
    if config["tile_width"] <= 0:
        raise ValueError("Tile width (number of bricks per row) must be greater than 0.")

half_brick = create_half_brick_aligned(config)  # 🔥 Ensure config is passed
full_brick = create_full_brick_aligned(config)  # 🔥 Ensure config is passed

print(f"Debug: Config being passed to create_half_brick_aligned: {config}")


def create_flemish_tile():
    """
    Creates a Flemish bond tile with proper alternating row patterns.
    Even rows are offset so the centres of half bricks align with the centres of full bricks in odd rows.
    """
    # Retrieve offsets and configuration values
    offset_X = config.get("offset_X", 0)  # X-axis offset between rows (horizontal shift between rows)
    row_repetition = config["row_repetition"]  # Number of rows in the tile
    tile_width = config["tile_width"]  # Number of bricks per row

    # Create an assembly for the entire tile
    tile_assembly = cq.Assembly()

    # Loop through rows to build the tile
    for i in range(row_repetition):
        # Create an assembly for the current row
        row_assembly = cq.Assembly()
        half_brick = create_half_brick_aligned(config)  # ✅ Fix here
        full_brick = create_full_brick_aligned(config)  # ✅ Fix here
        # Step 1: Determine X-offset for the entire row
        row_x_offset = 0
        if i % 2 != 0:  # For even rows only
            row_x_offset = -config["brick_length"] / 1.5  # Offset even rows to align centres

        # Step 2: Initialize the X-offset for bricks in this row
        x_offset = row_x_offset

        # Step 3: Add bricks to the row
        for j in range(tile_width):
            if j % 2 == 0:  # Add a full brick
                row_assembly.add(
                    full_brick,
                    loc=cq.Location(cq.Vector(x_offset, 0, 0)),
                    name=f"Full Brick Row{i}-Col{j}"
                )
                x_offset += config["brick_length"]  # Increment for the next position
            else:  # Add a half brick
                row_assembly.add(
                    half_brick,
                    loc=cq.Location(cq.Vector(x_offset, 0, 0)),
                    name=f"Half Brick Row{i}-Col{j}"
                )
                x_offset += config["brick_length"] / 2  # Increment for the next position

        # Step 4: Calculate Z-offset for the row to ensure proper stacking
        z_offset = i * config["brick_height"]

        # Step 5: Add the row assembly to the tile with calculated offsets
        tile_assembly.add(
            row_assembly,
            loc=cq.Location(cq.Vector(offset_X * i, 0, z_offset)),
            name=f"Row {i}"
        )

    return tile_assembly


# Main execution
if __name__ == "__main__":
    tile = create_flemish_tile()
    show_object(tile, name=config["file_name"])  # 👈 Dynamically names the model in viewer
    export_tile(tile, config, version="v2.0", cache_results=True)  # 🔥 Uses YAML file_name
