import os
import sys
import django
import cadquery as cq
from ocp_vscode import show_object  # Visualization for VS Code

# Add project root to sys.path for modular imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

# Import configuration, geometry, and file export functions
from resources.configs.yaml_config import load_config, validate_config, get_default_config_path
from resources.helpers.file_helper import export_tile
from resources.helpers.brick_geometry import assemble_tile

from django.conf import settings

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railworks_project.settings")
django.setup()

# Load and validate configuration
tile_type = "bricks"
config_path = get_default_config_path(tile_type)
config = load_config(config_path)
validate_config(config, tile_type)

# Generate tile
tile = assemble_tile(config)

# Visualize in OCP Viewer
show_object(tile, name="Flemish Bond Tile")

# Export tile
export_tile(tile, version="v2.0", tile_type=tile_type, export_formats=config["export_formats"])
