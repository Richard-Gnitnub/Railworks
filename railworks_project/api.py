from cad_pipeline.api import router as resources_router
from ninja import NinjaAPI

api = NinjaAPI()


api.add_router("/cad_pipeline/", cad_pipeline_router)
