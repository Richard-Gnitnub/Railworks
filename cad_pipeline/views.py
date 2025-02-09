from django.shortcuts import render
from django.http import JsonResponse
from .models import Assembly, Parameter
from django.shortcuts import render
from django.http import JsonResponse
from .models import Assembly, Parameter
from cad_pipeline.cad_engine.assemblies.generate_component import generate_and_export_component

def structure_selection(request):
    """
    Loads the selection UI.
    """
    return render(request, "structure_selection.html")

def dynamic_form_update(request):
    """
    Dynamically updates the form fields based on selected structure.
    """
    selected_type = request.GET.get("type")

    # Get all parameters for this type of structure
    parameters = Parameter.objects.filter(assembly__type=selected_type)

    return render(request, "partials/parameter_fields.html", {"parameters": parameters})

def generate_model(request):
    """
    Generates a model and provides a secure download link from the database.
    """
    component_id = request.GET.get("component_id")
    file_format = request.GET.get("file-format", "stl")

    try:
        component = Assembly.objects.get(id=component_id)
        parameters = {p.key: p.value for p in component.parameters.all()}

        # Generate and store in DB
        file_url = generate_and_export_component(component, parameters, file_format)

        return JsonResponse({"download_url": file_url})

    except Assembly.DoesNotExist:
        return JsonResponse({"error": "Component not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)