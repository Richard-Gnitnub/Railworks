import importlib
import logging
import cadquery as cq
from ocp_vscode import show_object
from cad_pipeline.models.parameter import Parameter
from cad_pipeline.models.assembly import Assembly  # ✅ Ensure correct import

logger = logging.getLogger(__name__)

def generate_component(component):
    """
    Dynamically loads the correct helper function based on component.type
    and generates the corresponding 3D model.
    """
    # ✅ Ensure component is an Assembly instance
    if not isinstance(component, Assembly):
        raise ValueError(f"Expected an Assembly instance, but got {type(component)}")

    parameters = {param.key: param.value for param in Parameter.objects.filter(assembly=component)}

    try:
        module_name = f"cad_pipeline.cad_engine.helpers.{component.type}_helper"
        module = importlib.import_module(module_name)

        function_name = "assemble_wall" if component.type == "wall" else "generate"
        if not hasattr(module, function_name):
            raise AttributeError(f"Module {module_name} does not contain '{function_name}()'.")

        generate_function = getattr(module, function_name)

        logger.info(f"Generating {component.type} using {module_name}.{function_name}()")
        print(f"🔧 Generating {component.type} using {module_name}.{function_name}()")

        model = generate_function(parameters)

        if not isinstance(model, cq.Workplane) and not isinstance(model, cq.Assembly):
            raise ValueError(f"Generated object from {module_name} is not a valid CadQuery model.")

        show_object(model)  

        return model

    except ModuleNotFoundError:
        logger.error(f"❌ No helper module found for component type: {component.type}")
        raise ValueError(f"No helper module found for component type: {component.type}")

    except AttributeError as e:
        logger.error(f"❌ {e}")
        raise ValueError(f"No '{function_name}' function found in {module_name}")
