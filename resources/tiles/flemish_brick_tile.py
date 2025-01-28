"""
Script: flemish_brick_tile.py
Description: Creates a Flemish bond tile using perfectly aligned bricks and mortar. Exports the result as a watertight STEP and STL file.
Dependencies: CadQuery, Django settings, OCP CAD Viewer, PyYAML
"""

import os
import sys
import django
import yaml
import cadquery as cq
from cadquery import exporters
from ocp_vscode import show_object  # Enable visualization in VS Code
from django.conf import settings

# Add the project root (where manage.py is located) to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railworks_project.settings")
django.setup()

# Debug: Verify Python Path
print("Python Path:", sys.path)

# Path to configuration file
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "../configs/")
CONFIG_FILE = os.path.join(CONFIG_DIR, "default_config.yaml")


def load_config(config_file=CONFIG_FILE):
    """Load configuration from a YAML file."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    with open(config_file, "r") as file:
        return yaml.safe_load(file)


def validate_config(config):
    """Ensure the YAML config contains all required keys."""
    required_keys = [
        "brick_length", "brick_width", "brick_height",
        "mortar_length", "mortar_width", "mortar_height",
    ]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")


# Load and validate configuration
config = load_config()
validate_config(config)

def create_full_brick_aligned(length=200, width=100, height=50):
    """Creates a full-sized brick using specified dimensions."""
    brick = cq.Workplane("XY").box(length, width, height)
    return brick.translate((length / 2, width / 2, height / 2))

def create_half_brick_aligned(length=100, width=100, height=50):
    """Creates a half-sized brick using specified dimensions."""
    brick = cq.Workplane("XY").box(length, width, height)
    return brick.translate((length / 2, width / 2, height / 2))

def create_mortar_row_layer(length=300, width=90, height=10):
    """Creates a mortar row layer using specified dimensions."""
    mortar = cq.Workplane("XY").box(length, width, height)
    return mortar.translate((length / 2, width / 2, height / 2))

# Create the first row
def create_first_row():
    """Creates the first row of bricks."""
    assembly = cq.Assembly()
    half_brick = create_half_brick_aligned()
    full_brick = create_full_brick_aligned()
    assembly.add(half_brick, loc=cq.Location(cq.Vector(0, 0, 0)), name="Half Brick")
    assembly.add(full_brick, loc=cq.Location(cq.Vector(config["brick_length"] / 2, 0, 0)), name="Full Brick")
    return assembly


# Create the second row (mortar layer)
def create_second_row():
    """Creates the second row (mortar layer)."""
    assembly = cq.Assembly()
    mortar_row = create_mortar_row_layer()
    assembly.add(mortar_row, loc=cq.Location(cq.Vector(0, 0, 0)), name="Mortar Row")
    return assembly


# Create the third row
def create_third_row():
    """Creates the third row of bricks."""
    assembly = cq.Assembly()
    full_brick = create_full_brick_aligned()
    half_brick = create_half_brick_aligned()
    assembly.add(full_brick, loc=cq.Location(cq.Vector(0, 0, 0)), name="Full Brick")
    assembly.add(half_brick, loc=cq.Location(cq.Vector(config["brick_length"], 0, 0)), name="Half Brick")
    return assembly


# Combine the rows into a three-row wall (the Flemish bond tile)
def create_flemish_tile():
    """Combines three rows into a Flemish bond tile."""
    first_row = create_first_row()
    second_row = create_second_row()
    third_row = create_third_row()

    wall_assembly = cq.Assembly()
    wall_assembly.add(first_row, loc=cq.Location(cq.Vector(0, 0, 0)), name="First Row")
    wall_assembly.add(second_row, loc=cq.Location(cq.Vector(0, 0, config["brick_height"])), name="Second Row")
    wall_assembly.add(third_row, loc=cq.Location(cq.Vector(0, 0, config["brick_height"] + config["mortar_height"])), name="Third Row")
    
    return wall_assembly


def export_tile(tile, version="v1.0"):
    """
    Exports the tile to STEP and STL files in a versioned directory.
    """
    output_dir = os.path.join(settings.MEDIA_ROOT, "resources", "tiles", f"v{version}")

    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Validate that the tile has valid geometry
    if not tile.children:
        raise ValueError("No shapes found to export. Tile is empty.")

    try:
        # File paths
        step_file_path = os.path.join(output_dir, f"flemish_tile_{version}.step")
        stl_file_path = os.path.join(output_dir, f"flemish_tile_{version}.stl")

        # Export files
        exporters.export(tile.toCompound(), step_file_path)
        exporters.export(tile.toCompound(), stl_file_path)

        print(f"STEP file exported to: {step_file_path}")
        print(f"STL file exported to: {stl_file_path}")
    except Exception as e:
        raise RuntimeError(f"Export failed: {e}")


# Main execution
if __name__ == "__main__":
    # Create and visualize the tile
    tile = create_flemish_tile()
    show_object(tile, name="Flemish Bond Tile")  # Visualize the tile in OCP Viewer
    # Export the tile
    export_tile(tile)
