from ninja import Router
from resources.helpers.tile_assembly import assemble_tile
from resources.configs.yaml_config import load_config
from resources.helpers.file_helper import export_tile

tile_router = Router()

@tile_router.post("/generate/")
def generate_tile(request, tile_type: str):
    """
    Generate a tile based on the provided tile type and configuration.
    """
    config_path = f"resources/configs/bricks/{tile_type}.yaml"
    config = load_config(config_path)

    # Dynamically assemble the tile
    tile = assemble_tile(config)

    # Export the tile
    export_formats = config.get("export_formats", ["step", "stl"])
    export_tile(tile, version="v1.0", tile_type=tile_type, export_formats=export_formats)

    return {"message": f"{tile_type.capitalize()} tile generated successfully."}
