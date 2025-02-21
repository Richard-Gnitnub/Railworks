import logging
import cadquery as cq
from cad_pipeline.cad_engine.globals.import_handler import import_step_subassembly
from cad_pipeline.cad_engine.helpers.tile_patterns.flemish_brick_tile_generator import generate_flemish_brick_tile
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from ocp_vscode import show_object
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.helpers.cutouts import apply_cutouts  # Updated to use the refactored function

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")


def generate_flemish_wall():
    """
    Generates a Flemish Brick Wall by:
    - Importing an existing wall STEP file from the database.
    - Triggering a tile rebuild if no STEP file exists.
    - Retrieving manual cutout placements from assembly parameters.
    - Exporting the final wall with modifications.
    """
    logging.info("🚀 Starting Flemish Brick Wall Assembly...")

    wall_assembly = retrieve_assembly("flemish_wall_generator")
    if not wall_assembly:
        return

    tile_model = import_tile_assembly(wall_assembly)
    if tile_model is None:
        return

    # Retrieve manual cutout placements from assembly parameters.
    manual_cutouts = wall_assembly.parameters.get("cutouts", [])
    if not manual_cutouts:
        logging.warning("⚠️ No manual cutouts defined; proceeding without cutouts.")

    wall_with_cutouts = apply_wall_cutouts(tile_model, manual_cutouts)
    if wall_with_cutouts is None:
        return

    export_flemish_wall(wall_with_cutouts, wall_assembly)

    logging.info("🎨 Displaying Flemish Wall in Viewer...")
    show_object(wall_with_cutouts, name="Flemish Wall")

    logging.info("✅ Flemish Brick Wall Generation Complete")
    return wall_with_cutouts


def retrieve_assembly(name):
    """
    Retrieves an assembly by name from the database.
    
    :param name: Assembly name.
    :return: Assembly object or None if not found.
    """
    try:
        return Assembly.objects.get(name=name)
    except Assembly.DoesNotExist:
        logging.error(f"❌ ERROR: Assembly `{name}` not found in the database.")
        return None


def import_tile_assembly(wall_assembly):
    """
    Imports or regenerates the Flemish Brick Tile assembly dynamically.
    
    The filename is derived directly from the wall assembly name to ensure consistency.
    """
    tile_assembly_name = "flemish_brick_tile_generator"
    tile_file_name = f"{wall_assembly.name}_{tile_assembly_name}.step"

    logging.info(f"🔄 Attempting to import `{tile_file_name}` from cache...")

    try:
        tile_model = import_step_subassembly(tile_file_name, generator_function=generate_flemish_brick_tile)
        if tile_model is None:
            logging.error(f"❌ ERROR: Failed to import or generate `{tile_file_name}`.")
            return None

        logging.info(f"✅ Successfully imported `{tile_file_name}`.")
        return tile_model
    except Exception as e:
        logging.error(f"❌ ERROR: Tile import/generation failed: {e}")
        return None


def apply_wall_cutouts(tile_model, cutouts):
    """
    Applies manual cutouts to the wall model using the provided cutouts list.
    
    :param tile_model: The base wall model.
    :param cutouts: A list of manually defined cutout dictionaries.
    :return: The modified wall model with applied cutouts.
    """
    try:
        logging.info("🛠 Applying manual cutouts to the wall...")
        return apply_cutouts(tile_model, cutouts)
    except Exception as e:
        logging.error(f"❌ ERROR: Failed to apply cutouts: {e}")
        return None


def export_flemish_wall(wall_model, wall_assembly):
    """
    Exports the Flemish Brick Wall using the global export handler.
    
    The filename is determined dynamically from the wall assembly.
    """
    try:
        export_config = {
            "export_formats": ["step", "stl"],
            "component": wall_assembly
        }
        exported_files = export_assembly(wall_model, **export_config)

        logging.info("✅ Wall Export Completed!")
        for fmt, file_data in exported_files.items():
            logging.info(f"   - Exported Format: {fmt.upper()}, Size: {len(file_data.file_data)} bytes")
    except Exception as e:
        logging.error(f"❌ ERROR: Failed to export wall: {e}")
