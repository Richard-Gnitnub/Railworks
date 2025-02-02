from ninja import NinjaAPI
from cad_pipeline.api.nmra_standard_api import router as nmra_router
from cad_pipeline.api.assembly_api import router as assembly_router
from cad_pipeline.api.parameter_api import router as parameter_router

api = NinjaAPI(
    title="Railworks API",
    version="1.0",
    description="API documentation for Railworks project",
    docs_url="/api/docs",  # ✅ Enables Swagger UI at `/api/docs/`
)

api.add_router("/nmra/", nmra_router)
api.add_router("/assemblies/", assembly_router)
api.add_router("/parameters/", parameter_router)
