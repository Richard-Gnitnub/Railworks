from ninja import NinjaAPI

# Initialize API instance
api = NinjaAPI(title="Railworks API", version="2.0", description="API for managing tile generation.")

def include_routers():
    """
    Dynamically import and attach routers to avoid circular imports.
    """
    from resources.api.config_api import config_router
    from resources.api.tile_api import tile_router

    api.add_router("/config/", config_router)
    api.add_router("/tile/", tile_router)

# Attach routers after API instance is created
include_routers()
