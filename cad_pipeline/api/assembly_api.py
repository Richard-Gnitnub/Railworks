from django.core.cache import cache
from django.shortcuts import get_object_or_404
from ninja import Router
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.api.schemas.assembly_schema import AssemblySchema, ErrorResponse

router = Router(tags=["Assemblies"])

@router.get("/assembly/{id}/", response={200: AssemblySchema, 404: ErrorResponse})
def get_assembly(request, id: int):
    """
    Retrieve a specific assembly, serving from cache when possible.
    Includes handling for soft-deleted records.
    """
    cache_key = f"assembly:{id}"
    cached_assembly = cache.get(cache_key)
    if cached_assembly:
        return cached_assembly
    assembly = get_object_or_404(Assembly.objects.all(), id=id)
    if assembly.is_deleted:
        return 404, {"error": "This assembly has been deleted."}
    cache.set(cache_key, assembly, timeout=86400)
    return assembly

@router.get("/assemblies/", response={200: list[AssemblySchema]})
def list_assemblies(request, model_type: str = None):
    """
    Retrieve all assemblies, optionally filtering by model type.
    Excludes soft-deleted records.
    """
    query = Assembly.objects.filter(is_deleted=False)
    if model_type:
        query = query.filter(model_type=model_type)
    return query

@router.post("/assemblies/", response={201: AssemblySchema, 400: ErrorResponse})
def create_assembly(request, payload: AssemblySchema):
    """
    Create a new assembly and cache it immediately.
    Ensures unique names and handles duplicate errors.
    """
    data = payload.dict(exclude_unset=True)
    if Assembly.objects.filter(name=data["name"], is_deleted=False).exists():
        return 400, {"error": "An assembly with this name already exists."}
    assembly = Assembly.objects.create(
        name=data["name"],
        model_type=data["model_type"],
        nmra_standard=data.get("nmra_standard"),
        metadata=data.get("metadata", {}),
    )
    cache_key = f"assembly:{assembly.id}"
    cache.set(cache_key, assembly, timeout=86400)
    return 201, assembly

@router.put("/assembly/{id}/", response={200: AssemblySchema, 404: ErrorResponse})
def update_assembly(request, id: int, payload: AssemblySchema):
    """
    Update an existing assembly and update cache.
    If metadata changes, the model's save() will handle version incrementation.
    """
    assembly = get_object_or_404(Assembly.objects.all(), id=id)
    if assembly.is_deleted:
        return 404, {"error": "This assembly has been deleted."}

    for attr, value in payload.dict(exclude_unset=True).items():
        if getattr(assembly, attr) != value:
            setattr(assembly, attr, value)
    assembly.save()  # Let the model's save() handle version and cache updates.
    cache_key = f"assembly:{id}"
    cache.set(cache_key, assembly, timeout=86400)
    return assembly

@router.delete("/assembly/{id}/", response={204: None, 404: ErrorResponse})
def delete_assembly(request, id: int):
    """
    Soft delete an assembly and remove it from cache.
    """
    assembly = get_object_or_404(Assembly.objects.all(), id=id)
    if assembly.is_deleted:
        return 404, {"error": "This assembly has already been deleted."}
    assembly.is_deleted = True
    assembly.save(update_fields=["is_deleted", "updated_at"])
    cache_key = f"assembly:{id}"
    cache.delete(cache_key)
    return None
