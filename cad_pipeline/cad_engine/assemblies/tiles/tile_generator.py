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
from cad_engine.export_handler import export_tile 
from cad_pipeline.configs.yaml_config import load_config, validate_config
from cad_engine.helpers.brick_geometry import create_full_brick_aligned, create_half_brick_aligned,config_to_tuple
from cad_engine.helpers.assemble_brick_tile import assemble_brick_tile
from django.conf import settings

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railworks_project.settings")
django.setup()

# Load and validate configuration
config_path = os.path.join(project_root, "cad_pipeline/configs/config_v2.yaml")
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

print(f"Debug: Config being passed to create_half_brick_aligned: {config}")

# Main execution
if __name__ == "__main__":
    tile = assemble_brick_tile(config)
    show_object(tile, name=config["file_name"])  # 👈 Dynamically names the model in viewer
    export_tile(tile, config, version="v2.0", cache_results=True)  # 🔥 Uses YAML file_name
