from ninja import Router
from typing import List
from ..models.parameter import Parameter
from .schemas.parameter_schema import ParameterSchema, ErrorResponse

router = Router(tags=["Parameters"])

@router.get(
    "/parameters/{parameter_type}/", 
    response={200: List[ParameterSchema], 404: ErrorResponse},
    summary="Retrieve parameters by type",
    description="Fetches all parameters that match the specified parameter type.",
)
def get_parameters_by_type(request, parameter_type: str):
    """
    Fetch parameters by the given parameter_type.
    """
    # Filter parameters by type
    parameters = Parameter.objects.filter(parameter_type=parameter_type)
    if not parameters.exists():
        # Return a 404 response if no parameters are found
        return 404, {"error": f"No parameters found for type '{parameter_type}'"}
    
    # Return a list of parameters
    return list(parameters.values("id", "name", "value", "parameter_type"))
