from ninja import NinjaAPI, File
from ninja.files import UploadedFile
import os
import yaml
from resources.configs.yaml_config import load_config, validate_config
from resources.tiles.flemish_brick_tile_v2 import create_flemish_tile, export_tile

api = NinjaAPI()

CONFIG_DIR = "resources/configs"

@api.get("/", tags=["General"])
def root(request):
    """
    API Root Endpoint - Provides a welcome message and link to documentation.
    """
    return {
        "message": "Welcome to the Railworks API!",
        "docs": "/api/docs"
    }


@api.post("/configs/")
def upload_config(request, file: UploadedFile = File(...)):
    """
    Endpoint to upload a YAML configuration file.
    """
    config_path = os.path.join(CONFIG_DIR, file.name)
    with open(config_path, "wb") as f:
        f.write(file.read())

    # Validate configuration
    config = load_config(config_path)
    validate_config(config)
    
    return {"message": "Configuration uploaded successfully!", "config_path": config_path}


@api.post("/tiles/generate/")
def generate_tile(request, config_name: str):
    """
    Endpoint to generate a Flemish bond tile.
    """
    config_path = os.path.join(CONFIG_DIR, config_name)
    config = load_config(config_path)
    validate_config(config)

    # Generate and export tile
    tile = create_flemish_tile()
    export_tile(tile)

    return {"message": "Tile generated and exported successfully!"}
