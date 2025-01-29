from ninja import Router
from resources.configs.yaml_config import load_config, validate_config, get_default_config_path

config_router = Router()

@config_router.get("/{tile_type}/config/")
def get_tile_config(request, tile_type: str):
    """
    Retrieve the configuration for a given tile type.
    """
    config_path = get_default_config_path(tile_type)
    config = load_config(config_path)
    validate_config(config, tile_type)
    return {"tile_type": tile_type, "config": config}
