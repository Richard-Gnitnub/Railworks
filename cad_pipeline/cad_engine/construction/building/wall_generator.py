import logging
import cadquery as cq
from datetime import datetime
from ocp_vscode import show_object

# Global import/export utilities
from cad_pipeline.cad_engine.globals.import_handler import import_step_subassembly
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from cad_pipeline.models.assembly import Assembly

# Import helpers for dimension calculation and cutouts
from cad_pipeline.cad_engine.helpers.calculate_wall_dimensions import calculate_wall_dimensions
from cad_pipeline.cad_engine.helpers.cutouts import apply_cutouts

# Import the global filename handler
from cad_pipeline.cad_engine.globals.filename_handler import generate_export_filename

# For metadata update of export timestamp
from cad_pipeline.cad_engine.globals.metadata_handler import update_last_export

# We'll import the tile generator function, which also expects an Assembly argument
from cad_pipeline.cad_engine.construction.building.brick_tile_generator import generate_flemish_brick_tile

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")


def generate_flemish_wall(wall_assembly: Assembly):
    """
    Generates a Flemish Brick Wall by:
      1. Calculating wall dimensions dynamically from brick geometry and tile parameters.
      2. Updating the wall assembly metadata with these dimensions.
      3. Importing an existing tile assembly STEP file from the database (or regenerating it).
      4. Optionally applying manual cutouts.
      5. Exporting and displaying the final wall model.
    
    :param wall_assembly: The Assembly object for the wall generator (e.g. "flemish_wall_generator").
    :return: A CadQuery Workplane representing the generated wall, or None if any step fails.
    """
    logging.info("🚀 Starting Flemish Brick Wall Generation...")

    # 1. Calculate wall dimensions (updates metadata in "flemish_wall_generator").
    dimensions = calculate_wall_dimensions()
    if dimensions is None:
        logging.error("❌ Failed to calculate wall dimensions.")
        return None
    logging.info(f"Calculated dimensions: {dimensions}")

    # 2. Import or regenerate the tile assembly.
    tile_model = import_tile_assembly(wall_assembly)
    if tile_model is None:
        logging.error("❌ Failed to import tile assembly.")
        return None

    # 3. Retrieve manual cutouts from the wall assembly parameters.
    manual_cutouts = wall_assembly.parameters.get("cutouts", [])
    if not manual_cutouts:
        logging.warning("⚠️ No manual cutouts defined; proceeding without cutouts.")

    wall_with_cutouts = apply_wall_cutouts(tile_model, manual_cutouts)
    if wall_with_cutouts is None:
        logging.error("❌ Failed to apply cutouts to wall.")
        return None

    # 4. Export the final wall model.
    export_flemish_wall(wall_with_cutouts, wall_assembly)

    # 5. Display the wall in the 3D viewer.
    logging.info("🎨 Displaying Flemish Wall in Viewer...")
    show_object(wall_with_cutouts, name="Flemish Wall")

    logging.info("✅ Flemish Brick Wall Generation Complete")
    return wall_with_cutouts


def import_tile_assembly(wall_assembly: Assembly) -> cq.Workplane:
    """
    Imports or regenerates the Flemish Brick Tile assembly dynamically, passing the tile assembly
    to `generate_flemish_brick_tile` if no STEP file is found in the DB.
    """
    tile_assembly_name = "flemish_brick_tile_generator"

    # 1. Retrieve the tile assembly from the DB
    from cad_pipeline.models import Assembly
    try:
        tile_assembly = Assembly.objects.get(name=tile_assembly_name)
    except Assembly.DoesNotExist:
        logging.error(f"❌ Tile assembly '{tile_assembly_name}' not found in DB.")
        return None

    # 2. Generate a standardized filename for the tile assembly
    tile_file_name = generate_export_filename(
        f"{wall_assembly.name}_{tile_assembly_name}", 
        "step",# e.g. "flemish_wall_generator_flemish_brick_tile_generator.step"
    )
    logging.info(f"🔄 Attempting to import '{tile_file_name}' from cache...")

    # 3. Provide a zero-argument function that calls `generate_flemish_brick_tile(tile_assembly)`
    def tile_generator_func():
        return generate_flemish_brick_tile(tile_assembly)

    try:
        tile_model = import_step_subassembly(tile_file_name, generator_function=tile_generator_func)
        if tile_model is None:
            logging.error(f"❌ ERROR: Failed to import or generate '{tile_file_name}'.")
            return None

        logging.info(f"✅ Successfully imported or regenerated '{tile_file_name}'.")
        return tile_model
    except Exception as e:
        logging.error(f"❌ ERROR: Tile import/generation failed: {e}")
        return None


def apply_wall_cutouts(tile_model: cq.Workplane, cutouts: list) -> cq.Workplane:
    """
    Applies manual cutouts to the wall model using the provided cutouts list.
    
    :param tile_model: The base wall model.
    :param cutouts: A list of manually defined cutout dictionaries.
    :return: The modified wall model with applied cutouts, or None on failure.
    """
    from cad_pipeline.cad_engine.helpers.cutouts import apply_cutouts
    try:
        logging.info("🛠 Applying manual cutouts to the wall...")
        return apply_cutouts(tile_model, cutouts)
    except Exception as e:
        logging.error(f"❌ ERROR: Failed to apply cutouts: {e}")
        return None


def export_flemish_wall(wall_model: cq.Workplane, wall_assembly: Assembly):
    """
    Exports the Flemish Brick Wall using the global export handler,
    then updates the export timestamp in the assembly metadata.
    
    :param wall_model: The final CadQuery Workplane representing the wall.
    :param wall_assembly: The Assembly object for this wall generator.
    """
    from cad_pipeline.cad_engine.globals.export_handler import export_assembly
    try:
        export_config = {
            "export_formats": ["step", "stl"],
            "component": wall_assembly
        }
        exported_files = export_assembly(wall_model, **export_config)
        logging.info("✅ Wall Export Completed!")
        for fmt, file_data in exported_files.items():
            logging.info(f"   - Exported Format: {fmt.upper()}, Size: {len(file_data.file_data)} bytes")

        from cad_pipeline.cad_engine.globals.metadata_handler import update_last_export
        update_last_export(wall_assembly.name, datetime.now().isoformat())
    except Exception as e:
        logging.error(f"❌ ERROR: Failed to export wall: {e}")


if __name__ == "__main__":
    # Example usage in Django shell:
    # from cad_pipeline.models import Assembly
    # wall_assembly = Assembly.objects.get(name="flemish_wall_generator")
    # wall_model = generate_flemish_wall(wall_assembly)
    pass
