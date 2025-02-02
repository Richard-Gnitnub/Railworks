from django.core.cache import cache
from ninja import Router, ModelSchema
from cad_pipeline.models import NMRAStandard

router = Router()

class NMRAStandardSchema(ModelSchema):
    class Config:
        model = NMRAStandard
        model_fields = "__all__"

@router.get("/nmra/{name}/", response=NMRAStandardSchema)
def get_nmra_standard(request, name: str):
    """Retrieve NMRA standard dynamically with caching."""
    cache_key = f"nmra:{name}"
    cached_nmra = cache.get(cache_key)

    if cached_nmra:
        return cached_nmra

    nmra = NMRAStandard.objects.get(name=name)
    cache
