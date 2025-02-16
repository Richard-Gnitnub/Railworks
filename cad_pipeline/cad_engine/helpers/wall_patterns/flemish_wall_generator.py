import logging
import cadquery as cq
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.globals.import_handler import import_step_subassembly
from cad_pipeline.cad_engine.helpers.tile_patterns.flemish_brick_tile_generator import generate_flemish_brick_tile
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from cad_pipeline.cad_engine.helpers.cutouts import apply_cutout
from ocp_vscode import show_object

# ✅ Configure Logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")


def generate_flemish_wall():
    """
    Generates a Flemish Brick Wall by:
    - Importing an existing wall STEP file from the database.
    - Triggering a tile rebuild if no STEP file exists.
    - Applying cutouts dynamically based on stored JSON parameters.
    - Exporting the final wall with modifications.
    """
    logging.info("🚀 Starting Flemish Brick Wall Assembly...")

    # ✅ **Step 1: Retrieve Wall Parameters**
    wall_assembly = get_assembly("flemish_wall_generator")  # ✅ FIXED: Match script name
    if not wall_assembly:
        return  # Exit if the wall assembly is missing

    cutouts = wall_assembly.parameters.get("cutouts", [])
    if not isinstance(cutouts, list):
        logging.error("❌ ERROR: Missing or invalid `cutouts` parameter in wall configuration.")
        return

    logging.info(f"📏 Retrieved {len(cutouts)} cutout(s) from database.")

    # ✅ **Step 2: Import or Generate Tile Assembly**
    tile_model = import_tile_assembly()
    if tile_model is None:
        return  # Exit if the tile import/generation fails

    # ✅ **Step 3: Apply Cutouts to the Wall**
    wall_with_cutouts = apply_wall_cutouts(tile_model, cutouts)
    if wall_with_cutouts is None:
        return  # Exit if cutout application fails

    # ✅ **Step 4: Export Wall**
    export_flemish_wall(wall_with_cutouts, wall_assembly)

    # ✅ **Step 5: Display Wall**
    logging.info("🎨 Displaying Flemish Wall in Viewer...")
    show_object(wall_with_cutouts, name="Flemish Wall")

    logging.info("✅ Flemish Brick Wall Generation Complete")
    return wall_with_cutouts


# ✅ **Helper Functions**
def get_assembly(name):
    """ Retrieves an assembly by name, handling missing records gracefully. """
    try:
        return Assembly.objects.get(name=name)
    except Assembly.DoesNotExist:
        logging.error(f"❌ ERROR: Assembly '{name}' not found in database.")
        return None


def import_tile_assembly():
    """ Imports or regenerates the Flemish Brick Tile assembly. """
    tile_file_name = "flemish_wall_generator_flemish_brick_tile_generator.step"  # ✅ FIXED: Match correct naming convention
    try:
        logging.info(f"🔄 Attempting to import `{tile_file_name}` from cache...")

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
    """ Applies cutouts to the wall model. """
    try:
        logging.info("🛠 Applying cutouts to the wall...")
        return apply_cutout(tile_model, cutouts)

    except Exception as e:
        logging.error(f"❌ ERROR: Failed to apply cutouts: {e}")
        return None


def export_flemish_wall(wall_model, wall_assembly):
    """ Exports the Flemish Brick Wall using a global export handler. """
    try:
        export_config = {
            "export_formats": ["step", "stl"],
            "component": wall_assembly  # ✅ FIXED: Let export handler determine filename
        }
        exported_files = export_assembly(wall_model, **export_config)

        logging.info("✅ Wall Export Completed!")
        for fmt, file_data in exported_files.items():
            logging.info(f"   - Exported Format: {fmt.upper()}, Size: {len(file_data.file_data)} bytes")

    except Exception as e:
        logging.error(f"❌ ERROR: Failed to export wall: {e}")
