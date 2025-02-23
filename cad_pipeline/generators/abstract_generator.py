import logging
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.generators.generator_strategy import IGenerator
from cad_pipeline.generators.concrete.concrete_brick_tile_generator import FlemishBrickTileGenerator
from cad_pipeline.generators.concrete.concrete_wall_generator import FlemishWallGenerator
from cad_pipeline.generators.concrete.concrete_building_generator import FlemishBuildingGenerator
from cad_pipeline.cad_engine.globals.import_handler import import_step_subassembly

# Registry mapping assembly types to concrete generator classes.
GENERATOR_REGISTRY = {
    "brick_tile": FlemishBrickTileGenerator,
    "wall": FlemishWallGenerator,
    "building": FlemishBuildingGenerator,
}

class GeneratorContext:
    def __init__(self, generator: IGenerator):
        self.generator = generator

    def set_strategy(self, generator: IGenerator):
        self.generator = generator

    def generate_assembly(self, assembly):
        return self.generator.generate(assembly)

def generate_object_with_cache(assembly_name: str):
    """
    Retrieves an assembly by name and attempts to import its exported STEP file.
    If the file is missing or invalid, the generator strategy is invoked to generate
    a new object. Child assemblies are processed recursively.
    """
    try:
        assembly = Assembly.objects.get(name=assembly_name)
    except Assembly.DoesNotExist:
        logging.error(f"Assembly '{assembly_name}' not found.")
        return None

    # Use custom filename from assembly parameters if provided, else default to assembly.name.
    base_filename = assembly.parameters.get("export_filename", assembly.name) if hasattr(assembly, "parameters") else assembly.name
    file_name = f"{base_filename}.step"
    
    def generator_function():
        assembly_type = assembly.type.lower()
        if assembly_type not in GENERATOR_REGISTRY:
            logging.error(f"No generator registered for assembly type '{assembly_type}'.")
            return None

        logging.info(f"Generating object for assembly '{assembly_name}' of type '{assembly_type}'.")
        generator_class = GENERATOR_REGISTRY[assembly_type]
        generator_strategy = generator_class()
        context = GeneratorContext(generator_strategy)
        generated_obj = context.generate_assembly(assembly)
        if generated_obj is None:
            logging.error(f"Generator for assembly '{assembly_name}' returned None.")
            return None

        # Process child assemblies recursively.
        children = assembly.children.all()
        if children:
            for child in children:
                child_obj = generate_object_with_cache(child.name)
                if child_obj is not None:
                    generated_obj = generated_obj.union(child_obj)
                    logging.info(f"Added child assembly '{child.name}' to parent '{assembly_name}'.")
        logging.info(f"Finished generating object for assembly '{assembly_name}'.")
        return generated_obj

    # Use caching mechanism: attempt to import STEP file, or generate if not available.
    return import_step_subassembly(file_name, generator_function)

if __name__ == "__main__":
    # For direct testing in a standalone context.
    obj = generate_object_with_cache("flemish_building_generator")
    if obj:
        from ocp_vscode import show_object
        show_object(obj, name="Abstract Generated Object")
