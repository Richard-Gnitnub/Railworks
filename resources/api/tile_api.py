from ninja import Router
from resources.helpers.file_helper import export_tile
from resources.helpers.brick_geometry import create_flemish_tile
from resources.configs.yaml_config import load_config, validate_config, get_default_config_path

tile_router = Router()

@tile_router.post("/generate/{tile_type}/")
def generate_tile(request, tile_type: str):
    """
    Generate a tile based on YAML configuration and return the file path.
    """
    config_path = get_default_config_path(tile_type)
    config = load_config(config_path)
    validate_config(config, tile_type)

    if tile_type == "bricks":
        tile = create_flemish_tile(config)
    else:
        return {"error": "Unsupported tile type"}

    file_path = export_tile(tile, version="v2.0", tile_type=tile_type, export_formats=config["export_formats"])
    return {"tile_type": tile_type, "exported_files": file_path}
