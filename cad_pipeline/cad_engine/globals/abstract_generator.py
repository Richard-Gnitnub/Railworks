import logging
from cad_pipeline.models.assembly import Assembly

# Import specific generator functions
from cad_pipeline.cad_engine.construction.building.brick_tile_generator import generate_flemish_brick_tile
from cad_pipeline.cad_engine.construction.building.wall_generator import generate_flemish_wall
from cad_pipeline.cad_engine.construction.building.building_generator import generate_flemish_building

# Registry mapping assembly types (or script keys) to generator functions.
# Here, each function is expected to accept an Assembly instance.
GENERATOR_REGISTRY = {
    "brick_tile": generate_flemish_brick_tile,
    "wall": generate_flemish_wall,
    "building": generate_flemish_building,
}

def generate_object(assembly_name: str):
    """
    Abstract generator that retrieves an assembly from the DB and dynamically calls
    the corresponding generator function based on the assembly type.
    
    If the assembly has child assemblies, it recursively generates those and unions
    their geometry with the parent.
    
    :param assembly_name: The name of the assembly to generate.
    :return: A CadQuery Workplane representing the generated object, or None if generation fails.
    """
    try:
        assembly = Assembly.objects.get(name=assembly_name)
    except Assembly.DoesNotExist:
        logging.error(f"Assembly '{assembly_name}' not found.")
        return None

    # Determine the generator key from assembly.type (should be like "wall", "building", etc.)
    assembly_type = assembly.type.lower()
    if assembly_type not in GENERATOR_REGISTRY:
        logging.error(f"No generator function registered for assembly type '{assembly_type}'.")
        return None

    logging.info(f"Generating object for assembly '{assembly_name}' of type '{assembly_type}'.")
    generator_func = GENERATOR_REGISTRY[assembly_type]
    # Now, call the generator function with the assembly as an argument.
    generated_obj = generator_func(assembly)
    if generated_obj is None:
        logging.error(f"Generator for assembly '{assembly_name}' returned None.")
        return None

    # If the assembly has children, recursively generate them and union their geometry.
    children = assembly.children.all()
    if children:
        for child in children:
            child_obj = generate_object(child.name)
            if child_obj is not None:
                generated_obj = generated_obj.union(child_obj)
                logging.info(f"Added child assembly '{child.name}' to parent '{assembly_name}'.")
    
    logging.info(f"Finished generating object for assembly '{assembly_name}'.")
    return generated_obj

if __name__ == "__main__":
    # Test the abstract generator
    obj = generate_object("flemish_building_generator")
    if obj:
        from ocp_vscode import show_object
        show_object(obj, name="Abstract Generated Object")
