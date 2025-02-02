from ninja import Schema
from typing import Any

class ParameterSchema(Schema):
    id: int
    name: str
    value: Any  # Flexible type for JSONField
    parameter_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "flemish",
                "value": "Flemish Bond",
                "parameter_type": "bond_pattern"
            }
        }

class ErrorResponse(Schema):
    error: str

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Parameter not found"
            }
        }

