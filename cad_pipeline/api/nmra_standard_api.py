from ninja import Router, Schema
from cad_pipeline.models import NMRAStandard
from django.db.models import Q

router = Router()

class NMRAStandardSchema(Schema):
    """Ensures API responses have correct types."""
    name: str
    scale_ratio: float
    gauge_mm: float
    clearance_mm: dict
    rail_profile: str

class ErrorResponse(Schema):
    """Defines a structured error response."""
    error: str

@router.get("/{name}/", response={200: NMRAStandardSchema, 404: ErrorResponse}, tags=["nmra"])
def get_nmra_standard(request, name: str):
    """Retrieve NMRA standard dynamically (case-insensitive & hyphen handling)."""

    formatted_name = name.replace("-", " ").title()

    nmra = NMRAStandard.objects.filter(Q(name__iexact=formatted_name)).first()

    if not nmra:
        return 404, {"error": f"NMRA Standard '{formatted_name}' not found"}

    return 200, NMRAStandardSchema(
        name=nmra.name,
        scale_ratio=nmra.scale_ratio,
        gauge_mm=nmra.gauge_mm,
        clearance_mm=nmra.clearance_mm,
        rail_profile=nmra.rail_profile,
    )
