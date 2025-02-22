import logging
from cad_pipeline.models.assembly import Assembly

# Import concrete generator classes.
from cad_pipeline.generators.concrete.concrete_brick_tile_generator import FlemishBrickTileGenerator
from cad_pipeline.generators.concrete.concrete_wall_generator import FlemishWallGenerator  # Assumes similar refactor exists.
from cad_pipeline.generators.concrete.concrete_building_generator import FlemishBuildingGenerator  # Assumes similar refactor exists.

# Registry mapping assembly types to concrete generator classes.
GENERATOR_REGISTRY = {
    "brick_tile": FlemishBrickTileGenerator,
    "wall": FlemishWallGenerator,
    "building": FlemishBuildingGenerator,
}

class GeneratorContext:
    def __init__(self, generator):
        self.generator = generator

    def set_strategy(self, generator):
        self.generator = generator

    def generate_assembly(self, assembly):
        return self.generator.generate(assembly)

def generate_object(assembly_name: str):
    """
    Abstract generator that retrieves an assembly from the database and dynamically
    applies the corresponding generator strategy.
    
    If the assembly has child assemblies, it recursively generates them and unions
    their geometry with the parent.
    
    :param assembly_name: The name of the assembly to generate.
    :return: A CadQuery Workplane representing the generated object, or None if generation fails.
    """
    try:
        assembly = Assembly.objects.get(name=assembly_name)
    except Assembly.DoesNotExist:
        logging.error(f"Assembly '{assembly_name}' not found.")
        return None

    # Determine the generator key from assembly.type (e.g. "wall", "building", etc.).
    assembly_type = assembly.type.lower()
    if assembly_type not in GENERATOR_REGISTRY:
        logging.error(f"No generator registered for assembly type '{assembly_type}'.")
        return None

    logging.info(f"Generating object for assembly '{assembly_name}' of type '{assembly_type}'.")

    # Instantiate the concrete generator strategy.
    generator_class = GENERATOR_REGISTRY[assembly_type]
    generator_strategy = generator_class()
    context = GeneratorContext(generator_strategy)

    # Generate the object using the selected strategy.
    generated_obj = context.generate_assembly(assembly)
    if generated_obj is None:
        logging.error(f"Generator for assembly '{assembly_name}' returned None.")
        return None

    # Recursively process child assemblies.
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
    # Test the abstract generator.
    obj = generate_object("flemish_building_generator")
    if obj:
        from ocp_vscode import show_object
        show_object(obj, name="Abstract Generated Object")
