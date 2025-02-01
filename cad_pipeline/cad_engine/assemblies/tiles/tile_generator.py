import os
import sys
import cadquery as cq
from ocp_vscode import show_object  # Enable visualization in VS Code

# 🔹 Ensure the project root (where `cad_pipeline/` is located) is in `sys.path`
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(PROJECT_ROOT)

# Import configuration and tile generation functions
from cad_engine.export_handler import export_tile
from cad_engine.helpers.brick_geometry import create_full_brick_aligned, create_half_brick_aligned, config_to_tuple
from cad_engine.helpers.assemble_brick_tile import assemble_brick_tile
from cad_engine.configs.config.config import load_config, validate_config  # Updated import

# Load Configuration
CONFIG_PATH = os.path.join(PROJECT_ROOT, "cad_engine/configs/config.yaml")
config = load_config(CONFIG_PATH)
validate_config(config)

# Main execution
if __name__ == "__main__":
    tile = assemble_brick_tile(config)
    show_object(tile, name=config["file_name"])
    export_tile(tile, config, version="v2.0", cache_results=True)
