from resources.api import router as resources_router
from ninja import NinjaAPI

api = NinjaAPI()


api.add_router("/resources/", resources_router)
