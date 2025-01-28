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
from resources.configs.yaml_config import load_config, validate_config
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

validate_tile_parameters()

# Geometry creation functions
def create_full_brick_aligned(length=config["brick_length"], width=config["brick_width"], height=config["brick_height"], chamfer=config["mortar_chamfer"]):
    """Creates a full-sized brick with chamfered edges to simulate mortar."""
    brick = (
        cq.Workplane("XY")
        .box(length, width, height)
        .edges("|Z or |X ")  # Select vertical edges
        .chamfer(chamfer)  # Apply a chamfer to simulate mortar
    )
    return brick.translate((length / 2, width / 2, height / 2))

def create_half_brick_aligned(length=config["brick_length"] / 2, width=config["brick_width"], height=config["brick_height"], chamfer=config["mortar_chamfer"]):
    """Creates a half-sized brick with chamfered edges to simulate mortar."""
    brick = (
        cq.Workplane("XY")
        .box(length, width, height)
        .edges("|Z or |X ")  # Select vertical edges
        .chamfer(chamfer)  # Apply a chamfer to simulate mortar
    )
    return brick.translate((length / 2, width / 2, height / 2))

def create_flemish_tile():
    """
    Creates a Flemish bond tile with alternating row patterns.
    Each row alternates between starting with a half brick and a full brick.
    """
    offset_X = config.get("offset_X", 0)
    offset_Y = config.get("offset_Y", 0)
    offset_Y = config.get("offset_Y", 0)
    row_repetition = config["row_repetition"]
    tile_width = config["tile_width"]

    tile_assembly = cq.Assembly()

    for i in range(row_repetition):
        row_assembly = cq.Assembly()
        half_brick = create_half_brick_aligned()
        full_brick = create_full_brick_aligned()

        # Determine starting brick for the row (alternate pattern)
        start_with_half_brick = (i % 2 == 0)

        for j in range(tile_width):
            x_offset = j * config["brick_length"]

            # Alternate starting brick pattern
            if start_with_half_brick:
                if j % 2 == 0:
                    row_assembly.add(half_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)), name=f"Half Brick Row{i}-Col{j}")
                else:
                    row_assembly.add(full_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)), name=f"Full Brick Row{i}-Col{j}")
            else:
                if j % 2 == 0:
                    row_assembly.add(full_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)), name=f"Full Brick Row{i}-Col{j}")
                else:
                    row_assembly.add(half_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)), name=f"Half Brick Row{i}-Col{j}")

        # Adjust vertical offset using offset_Z
        z_offset = i * config["brick_height"]  # Add vertical alignment
    tile_assembly.add(row_assembly, loc=cq.Location(cq.Vector(0, 0, z_offset)), name=f"Row {i}")

    return tile_assembly


def export_tile(tile, version="v2.0"):
    """
    Exports the tile to specified formats in a versioned directory.
    """
    output_dir = os.path.join(settings.MEDIA_ROOT, "resources", "tiles", f"v{version}")
    os.makedirs(output_dir, exist_ok=True)

    export_formats = config.get("export_formats", ["step", "stl"])
    for fmt in export_formats:
        file_path = os.path.join(output_dir, f"flemish_tile_{version}.{fmt}")
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

# Main execution
if __name__ == "__main__":
    # Create and visualize the tile
    tile = create_flemish_tile()
    show_object(tile, name="Flemish Bond Tile V2")  # Visualize the tile in OCP Viewer
    # Export the tile
    export_tile(tile)
