from ninja import Schema
from typing import Optional, Dict

class AssemblySchema(Schema):
    """Defines the response structure for an Assembly object."""
    id: int
    name: str
    model_type: str
    nmra_standard_id: Optional[int]  # ForeignKey to NMRAStandard
    metadata: Dict  # JSONField in Django
    created_at: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Warehouse Wall 3m x 2m",
                "model_type": "wall",
                "nmra_standard_id": 1,
                "metadata": {
                    "brick_length": 250,
                    "brick_width": 120,
                    "brick_height": 60,
                    "mortar_chamfer": 5,
                    "bond_pattern": "flemish"
                },
                "created_at": "2025-02-02T12:00:00Z"
            }
        }

class ErrorResponse(Schema):
    """Defines a structured error response."""
    error: str

    class Config:
        schema_extra = {
            "example": {
                "error": "Assembly not found"
            }
        }
