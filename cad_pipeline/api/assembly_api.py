from django.core.cache import cache
from django.shortcuts import get_object_or_404
from ninja import Router
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.api.schemas.assembly_schema import AssemblySchema, ErrorResponse

router = Router(tags=["Assemblies"])

# ✅ Retrieve a Single Assembly (with caching)
@router.get("/assembly/{id}/", response={200: AssemblySchema, 404: ErrorResponse})
def get_assembly(request, id: int):
    """Retrieve a specific assembly with caching."""
    cache_key = f"assembly:{id}"
    
    # Check cache first
    cached_assembly = cache.get(cache_key)
    if cached_assembly:
        return cached_assembly  # ✅ Serve from cache

    # Retrieve from DB if not cached
    assembly = get_object_or_404(Assembly, id=id)

    # Store in cache for 24 hours (86400 seconds)
    cache.set(cache_key, assembly, timeout=86400)
    return assembly

# ✅ Retrieve All Assemblies (Optional Model Type Filtering)
@router.get("/assemblies/", response={200: list[AssemblySchema]})
def list_assemblies(request, model_type: str = None):
    """Retrieve all assemblies, optionally filtering by model type."""
    query = Assembly.objects.all()
    if model_type:
        query = query.filter(model_type=model_type)
    
    return query

# ✅ Create or Overwrite an Assembly (Cache it Immediately)
@router.post("/assemblies/", response={200: AssemblySchema, 201: AssemblySchema})
def create_or_update_assembly(request, payload: AssemblySchema):
    """Creates a new assembly or updates an existing one if the name already exists."""
    data = payload.dict(exclude_unset=True)  # ✅ Prevents `id` from being passed

    # ✅ Check if an assembly with the same name exists
    assembly, created = Assembly.objects.update_or_create(
        name=data["name"],
        defaults={
            "model_type": data["model_type"],
            "nmra_standard": data.get("nmra_standard"),
            "metadata": data.get("metadata", {}),
        },
    )

    # ✅ Invalidate and update cache
    cache_key = f"assembly:{assembly.id}"
    cache.delete(cache_key)
    cache.set(cache_key, assembly, timeout=86400)

    return (201, assembly) if created else (200, assembly)  # 201 if new, 200 if updated

# ✅ Soft Delete an Assembly (Invalidate Cache)
@router.delete("/assembly/{id}/", response={204: None, 404: ErrorResponse})
def delete_assembly(request, id: int):
    """Soft delete an assembly and remove it from cache."""
    assembly = get_object_or_404(Assembly, id=id)

    # Soft delete the record
    assembly.is_deleted = True
    assembly.save()

    # Invalidate cache
    cache_key = f"assembly:{id}"
    cache.delete(cache_key)

    return None  # 204 No Content
