from ninja import Router, ModelSchema
from cad_pipeline.models import Parameter

router = Router()

class ParameterSchema(ModelSchema):
    class Config:
        model = Parameter
        model_fields = "__all__"

@router.get("/parameters/{parameter_type}/", response=list[ParameterSchema])
def get_parameters_by_type(request, parameter_type: str):
    """Retrieve configurable settings (bond patterns, export formats, constraints)."""
    return Parameter.objects.filter(parameter_type=parameter_type)
