from ninja import Schema
from typing import Optional, Dict
from datetime import datetime

class AssemblySchema(Schema):
    name: str
    model_type: str
    metadata: dict
    nmra_standard_id: Optional[int] = None
    created_at: Optional[datetime] = None  # Read-only
    updated_at: Optional[datetime] = None  # Read-only

    class Config:
        json_schema_extra = {
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

class CachedAssemblyResponse(Schema):
    """Defines the response when serving from cache."""
    source: str  # Indicates whether it's from cache or database
    assembly: AssemblySchema

    class Config:
        json_schema_extra = {
            "example": {
                "source": "cache",
                "assembly": {
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
        }

class ErrorResponse(Schema):
    """Defines a structured error response."""
    error: str

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Assembly not found"
            }
        }
