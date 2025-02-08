from .nmra_standard_api import router as nmra_router
from .assembly_api import router as assembly_router
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router("/nmra/", nmra_router)
api.add_router("/assemblies/", assembly_router)
