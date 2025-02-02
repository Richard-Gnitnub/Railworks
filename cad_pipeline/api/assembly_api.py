# cad_pipeline/api/assembly_api.py

from django.core.cache import cache
from ninja import Router
from ninja.errors import HttpError
from typing import List, Optional
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.api.schemas.assembly_schema import AssemblySchema, ErrorResponse

# Create Router with Tags for Organization in Swagger UI
router = Router(tags=["Assemblies"])

@router.get(
    "/assembly/{id}/",
    response={200: AssemblySchema, 404: ErrorResponse},
    summary="Get Assembly by ID",
    description="Retrieves a specific assembly by its ID. Uses caching to improve performance."
)
def get_assembly(request, id: int):
    """
    Retrieve a specific assembly with caching.
    Returns 404 if the assembly is not found.
    """
    cache_key = f"assembly:{id}"
    cached_assembly = cache.get(cache_key)

    if cached_assembly:
        return cached_assembly

    try:
        assembly = Assembly.objects.get(id=id)
        # Serialize and cache the response
        serialized_assembly = AssemblySchema.from_orm(assembly)
        cache.set(cache_key, serialized_assembly.dict(), timeout=3600)
        return serialized_assembly
    except Assembly.DoesNotExist:
        raise HttpError(404, "Assembly with the given ID was not found.")


@router.get(
    "/assembly/",
    response={200: List[AssemblySchema]},
    summary="List Assemblies",
    description="Retrieves all assemblies. Optionally filter by model type."
)
def list_assemblies(request, model_type: Optional[str] = None):
    """
    Retrieve all assemblies, optionally filtering by model type.
    Returns a list of assemblies.
    """
    query = Assembly.objects.all()
    if model_type:
        query = query.filter(model_type=model_type)
    return query
