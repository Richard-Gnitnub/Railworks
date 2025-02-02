from django.core.cache import cache
from ninja import Router, ModelSchema
from cad_pipeline.models import Assembly

router = Router()

class AssemblySchema(ModelSchema):
    class Config:
        model = Assembly
        model_fields = "__all__"

@router.get("/assemblies/{id}/", response=AssemblySchema)
def get_assembly(request, id: int):
    """Retrieve a specific assembly with caching."""
    cache_key = f"assembly:{id}"
    cached_assembly = cache.get(cache_key)

    if cached_assembly:
        return cached_assembly

    assembly = Assembly.objects.get(id=id)
    cache.set(cache_key, assembly, timeout=3600)  # Cache for 1 hour
    return assembly

@router.get("/assemblies/", response=list[AssemblySchema])
def list_assemblies(request, model_type: str = None):
    """Retrieve all assemblies, optionally filtering by model type."""
    query = Assembly.objects.all()
    if model_type:
        query = query.filter(model_type=model_type)
    return query
