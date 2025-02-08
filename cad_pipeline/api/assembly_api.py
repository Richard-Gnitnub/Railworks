from django.core.cache import cache
from django.shortcuts import get_object_or_404
from ninja import Router
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.api.schemas.assembly_schema import AssemblySchema, ErrorResponse

router = Router(tags=["Assemblies"])

# ✅ Retrieve a Single Assembly (Cache Enabled)
@router.get("/assembly/{id}/", response={200: AssemblySchema, 404: ErrorResponse})
def get_assembly(request, id: int):
    """Retrieve a specific assembly, serving from cache when possible."""
    cache_key = f"assembly:{id}"
    
    cached_assembly = cache.get(cache_key)
    if cached_assembly:
        return cached_assembly  # ✅ Serve from cache

    assembly = get_object_or_404(Assembly, id=id)

    # Store the latest version in cache
    cache.set(cache_key, assembly, timeout=86400)
    return assembly

# ✅ Retrieve All Assemblies (Optional Model Type Filtering)
@router.get("/assemblies/", response={200: list[AssemblySchema]})
def list_assemblies(request, model_type: str = None):
    """Retrieve all assemblies, optionally filtering by model type."""
    query = Assembly.objects.filter(is_deleted=False)  # Exclude soft-deleted assemblies
    if model_type:
        query = query.filter(model_type=model_type)
    
    return query

# ✅ Create a New Assembly (Does Not Overwrite)
@router.post("/assemblies/", response={201: AssemblySchema})
def create_assembly(request, payload: AssemblySchema):
    """Creates a new assembly and caches it immediately."""
    data = payload.dict(exclude_unset=True)

    # Ensure a new unique assembly is created
    assembly = Assembly.objects.create(
        name=data["name"],
        model_type=data["model_type"],
        nmra_standard=data.get("nmra_standard"),
        metadata=data.get("metadata", {}),
    )

    # ✅ Cache the new assembly
    cache_key = f"assembly:{assembly.id}"
    cache.set(cache_key, assembly, timeout=86400)

    return assembly  # ✅ Returns HTTP 201 Created

# ✅ Update an Existing Assembly (Increment Version)
@router.put("/assembly/{id}/", response={200: AssemblySchema, 404: ErrorResponse})
def update_assembly(request, id: int, payload: AssemblySchema):
    """Updates an existing assembly, increments version if metadata changes, and updates cache."""
    assembly = get_object_or_404(Assembly, id=id)

    updated_fields = []
    for attr, value in payload.dict().items():
        if getattr(assembly, attr) != value:
            setattr(assembly, attr, value)
            updated_fields.append(attr)

    if "metadata" in updated_fields:
        assembly.version += 1  # ✅ Increment version only if metadata changed

    assembly.save(update_fields=updated_fields + ["version", "updated_at"])

    # ✅ Invalidate and update cache
    cache_key = f"assembly:{id}"
    cache.delete(cache_key)
    cache.set(cache_key, assembly, timeout=86400)

    return assembly  # ✅ Returns HTTP 200 OK

# ✅ Soft Delete an Assembly (Invalidate Cache)
@router.delete("/assembly/{id}/", response={204: None, 404: ErrorResponse})
def delete_assembly(request, id: int):
    """Soft delete an assembly and remove it from cache."""
    assembly = get_object_or_404(Assembly, id=id)

    # ✅ Soft delete the record
    assembly.is_deleted = True
    assembly.save(update_fields=["is_deleted"])

    # ✅ Invalidate cache
    cache_key = f"assembly:{id}"
    cache.delete(cache_key)

    return None  # ✅ Returns HTTP 204 No Content
