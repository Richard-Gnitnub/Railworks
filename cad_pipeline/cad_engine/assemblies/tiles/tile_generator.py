"""
Script: tile_generator.py
Description: Generates a Flemish bond tile with modular configuration and reusable row generation.
Dependencies: CadQuery, Django, YAML, Export Handlers, Brick Helpers.
"""

import os
import sys
import cadquery as cq
from ocp_vscode import show_object  # Enable visualization in VS Code

# 🔹 Ensure the project root (where `cad_pipeline/` is located) is in `sys.path`
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, PROJECT_ROOT)  # ✅ Use `insert(0, …)` instead of `append()` to prioritize this path

# 🔹 Configure Django settings ONLY if required
try:
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railworks_project.settings")
    django.setup()
except ModuleNotFoundError:
    print("Warning: Django not found. Running in non-Django mode.")

# 🔹 Import configuration and tile generation functions
from cad_engine.export_handler import export_tile
from cad_engine.helpers.brick_geometry import create_full_brick_aligned, create_half_brick_aligned, config_to_tuple
from cad_engine.helpers.assemble_brick_tile import assemble_brick_tile
from cad_engine.configs.config import load_config, validate_config  # ✅ Updated import

# 🔹 Load Configuration
CONFIG_PATH = os.path.join(PROJECT_ROOT, "cad_engine/configs/config.yaml")
config = load_config(CONFIG_PATH)
validate_config(config)

# 🔹 Validate tile configuration values
def validate_tile_parameters():
    """Ensures valid YAML configuration for tile dimensions and repetition settings."""
    if config["row_repetition"] <= 0:
        raise ValueError("Row repetition must be greater than 0.")
    if config["brick_length"] <= 0 or config["brick_width"] <= 0 or config["brick_height"] <= 0:
        raise ValueError("Brick dimensions must be greater than 0.")
    if config["tile_width"] <= 0:
        raise ValueError("Tile width (number of bricks per row) must be greater than 0.")

print(f"Debug: Config being passed to create_half_brick_aligned: {config}")

# 🔹 Main Execution
if __name__ == "__main__":
    try:
        tile = assemble_brick_tile(config)
        show_object(tile, name=config["file_name"])  # 👈 Dynamically names the model in the viewer
        export_tile(tile, config, version="v2.0", cache_results=True)  # 🔥 Uses YAML `file_name`
    except Exception as e:
        print(f"❌ Error generating tile: {e}")
