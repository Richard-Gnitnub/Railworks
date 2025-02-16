import logging
import cadquery as cq
from cad_pipeline.cad_engine.globals.import_handler import import_step_subassembly
from cad_pipeline.cad_engine.helpers.tile_patterns.flemish_brick_tile_generator import generate_flemish_brick_tile
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from cad_pipeline.cad_engine.helpers.cutouts import apply_cutout
from cad_pipeline.cad_engine.globals.regular_grid import regular_grid
from ocp_vscode import show_object
from cad_pipeline.models.assembly import Assembly

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")


def generate_flemish_wall():
    """
    Generates a Flemish Brick Wall by:
    - Importing an existing wall STEP file from the database.
    - Triggering a tile rebuild if no STEP file exists.
    - Generating a grid-based cutout pattern dynamically.
    - Exporting the final wall with modifications.
    """
    logging.info("🚀 Starting Flemish Brick Wall Assembly...")

    wall_assembly = retrieve_assembly("flemish_wall_generator")
    if not wall_assembly:
        return

    tile_model = import_tile_assembly(wall_assembly)
    if tile_model is None:
        return

    grid = generate_wall_grid()
    if grid is None:
        return

    wall_with_cutouts = apply_wall_cutouts(tile_model, grid)
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


def generate_wall_grid():
    """
    Generates a grid for cutouts based on wall dimensions derived from the tile generator.
    
    It uses parameters from both the tile assembly and the wall assembly.
    """
    tile_assembly = retrieve_assembly("flemish_brick_tile_generator")
    if not tile_assembly:
        logging.error("❌ ERROR: `flemish_brick_tile_generator` assembly not found in DB.")
        return None

    tile_parameters = tile_assembly.parameters
    if "tile_width" not in tile_parameters or "row_repetition" not in tile_parameters:
        logging.error("❌ ERROR: Missing `tile_width` or `row_repetition` in `flemish_brick_tile_generator`.")
        return None

    tile_width = tile_parameters["tile_width"]
    row_repetition = tile_parameters["row_repetition"]

    brick_geometry = retrieve_assembly("brick_geometry")
    if not brick_geometry:
        logging.error("❌ ERROR: `brick_geometry` assembly not found in DB.")
        return None

    brick_length = brick_geometry.parameters.get("brick_length", 215)
    brick_height = brick_geometry.parameters.get("brick_height", 65)

    wall_width = tile_width * brick_length
    wall_height = row_repetition * brick_height

    logging.info(f"📏 Computed Wall Dimensions → Width: {wall_width}, Height: {wall_height}")

    wall_assembly = retrieve_assembly("flemish_wall_generator")
    if not wall_assembly:
        logging.error("❌ ERROR: `flemish_wall_generator` assembly not found in DB.")
        return None

    grid_parameters = wall_assembly.parameters.get("grid_parameters", {})

    return regular_grid(
        width=wall_width,
        height=wall_height,
        spacing_x=grid_parameters.get("grid_spacing_x", 100),
        spacing_y=grid_parameters.get("grid_spacing_y", 100),
        offset_x=grid_parameters.get("grid_offset_x", 0),
        offset_y=grid_parameters.get("grid_offset_y", 0),
    )


def apply_wall_cutouts(tile_model, grid):
    """
    Applies cutouts to the wall model using the provided grid.
    """
    try:
        logging.info("🛠 Applying cutouts to the wall using grid-based approach...")
        return apply_cutout(tile_model, grid)
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
