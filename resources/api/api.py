from ninja import NinjaAPI
from resources.api.tile_api import tile_router

api = NinjaAPI()

def include_routers():
    api.add_router("/tiles/", tile_router)

include_routers()
