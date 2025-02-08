import importlib
import logging
import cadquery as cq
from ocp_vscode import show_object
from cad_pipeline.models.assembly import Assembly

logger = logging.getLogger(__name__)

def generate_component(component):
    """
    Dynamically loads the correct helper function based on component.type
    and generates the corresponding 3D model.

    - Uses MPTT hierarchy to retrieve children instead of a parameter model.
    - Ensures parent-child relationships are correctly handled.
    - Loads correct module dynamically based on component type.
    """
    if not isinstance(component, Assembly):
        raise ValueError(f"Expected an Assembly instance, but got {type(component)}")

    # ✅ Reload from DB to ensure the latest instance
    component = Assembly.objects.get(pk=component.pk)

    # ✅ Fetch child assemblies instead of parameters
    children = Assembly.objects.filter(parent=component)

    if not children.exists():
        logger.warning(f"❌ No children found for {component.name}.")
    else:
        logger.info(f"✅ {component.name} has {children.count()} children:")
        for child in children:
            logger.info(f"🔹 Child: {child.name} (Type: {child.type})")

    try:
        # ✅ Dynamically determine the correct helper module
        module_name = f"cad_pipeline.cad_engine.helpers.{component.type}_helper"
        module = importlib.import_module(module_name)

        # ✅ Select the correct function to call
        function_name = "assemble_wall" if component.type == "wall" else "generate"
        if not hasattr(module, function_name):
            raise AttributeError(f"Module {module_name} does not contain '{function_name}()'.")

        generate_function = getattr(module, function_name)

        logger.info(f"🔧 Generating {component.type} using {module_name}.{function_name}()")
        print(f"🔧 Generating {component.type} using {module_name}.{function_name}()")

        # ✅ Pass child assemblies instead of parameters
        model = generate_function(children)

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

