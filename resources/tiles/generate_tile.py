import os
import sys
import django
from ocp_vscode import show_object

# Ensure Python finds `resources/`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# ✅ **Manually configure Django settings**
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railworks_project.settings")
django.setup()  # ✅ This initializes Django settings manually

# Import necessary modules AFTER setting up Django
from django.conf import settings
from resources.configs.yaml_config import load_config, validate_config, get_default_config_path
from resources.helpers.tile_assembly import assemble_tile
from resources.helpers.file_helper import export_tile

# Load default config path (fallback to "brick_tile" if type is not set)
default_config_path = get_default_config_path("brick_tile")  # Uses correct filename
temp_config = load_config(default_config_path)

# Extract actual tile type from the loaded config
tile_type = temp_config.get("tile_type", "brick_tile")  # Defaults to "brick_tile" if missing

# Load correct config file based on actual tile type
config_path = get_default_config_path(tile_type)
config = load_config(config_path)

# Validate the extracted config
validate_config(config, tile_type)

# Generate the tile dynamically
tile = assemble_tile(config)

# ✅ **Ensure `MEDIA_ROOT` exists**
if not os.path.exists(settings.MEDIA_ROOT):
    os.makedirs(settings.MEDIA_ROOT)

# Export the tile
export_tile(tile, version="v2.0", tile_type=tile_type, export_formats=config["export_formats"])

print(f"✅ Tile generation and export completed for {tile_type}!")

     # Visualize the tile
show_object(tile, name="Flemish Bond Tile")