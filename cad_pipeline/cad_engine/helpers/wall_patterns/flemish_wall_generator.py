import logging
import tempfile
import cadquery as cq
from datetime import datetime
from ocp_vscode import show_object

# Global import/export utilities
from cad_pipeline.cad_engine.globals.import_handler import import_step_subassembly
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from cad_pipeline.models.assembly import Assembly

# Import helpers
from cad_pipeline.cad_engine.helpers.calculate_wall_dimensions import calculate_wall_dimensions
from cad_pipeline.cad_engine.helpers.cutouts import apply_cutouts

# Import the global filename handler
from cad_pipeline.cad_engine.globals.filename_handler import generate_export_filename

# Import the tile generator to auto-regenerate if needed
from cad_pipeline.cad_engine.helpers.tile_patterns.flemish_brick_tile_generator import generate_flemish_brick_tile

# For metadata update of export timestamp
from cad_pipeline.cad_engine.globals.metadata_handler import update_last_export

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def generate_flemish_wall():
    """
    Generates a Flemish Brick Wall by:
      - Calculating wall dimensions dynamically from brick geometry and tile parameters.
      - Updating the wall assembly metadata with these dimensions.
      - Importing an existing wall STEP file from the database (or regenerating it).
      - Optionally applying manual cutouts.
      - Exporting and displaying the final wall model.
    """
    logging.info("🚀 Starting Flemish Brick Wall Generation...")

    wall_assembly = retrieve_assembly("flemish_wall_generator")
    if not wall_assembly:
        return None

    dimensions = calculate_wall_dimensions()
    if dimensions is None:
        logging.error("❌ Failed to calculate wall dimensions.")
        return None
    logging.info(f"Calculated dimensions: {dimensions}")

    tile_model = import_tile_assembly(wall_assembly)
    if tile_model is None:
        return None

    manual_cutouts = wall_assembly.parameters.get("cutouts", [])
    if not manual_cutouts:
        logging.warning("⚠️ No manual cutouts defined; proceeding without cutouts.")

    wall_with_cutouts = apply_wall_cutouts(tile_model, manual_cutouts)
    if wall_with_cutouts is None:
        return None

    export_flemish_wall(wall_with_cutouts, wall_assembly)

    logging.info("🎨 Displaying Flemish Wall in Viewer...")
    show_object(wall_with_cutouts, name="Flemish Wall")

    logging.info("✅ Flemish Brick Wall Generation Complete")
    return wall_with_cutouts

def retrieve_assembly(name: str):
    """
    Retrieves an assembly by name from the database.
    
    :param name: Assembly name.
    :return: Assembly object or None if not found.
    """
    try:
        return Assembly.objects.get(name=name)
    except Assembly.DoesNotExist:
        logging.error(f"❌ ERROR: Assembly '{name}' not found in the database.")
        return None

def import_tile_assembly(wall_assembly):
    """
    Imports or regenerates the Flemish Brick Tile assembly dynamically.
    
    The filename is generated using the global filename handler to ensure consistency.
    """
    tile_assembly_name = "flemish_brick_tile_generator"
    tile_file_name = generate_export_filename(f"{wall_assembly.name}_{tile_assembly_name}", "step")
    logging.info(f"🔄 Attempting to import '{tile_file_name}' from cache...")

    try:
        tile_model = import_step_subassembly(tile_file_name, generator_function=generate_flemish_brick_tile)
        if tile_model is None:
            logging.error(f"❌ ERROR: Failed to import or generate '{tile_file_name}'.")
            return None

        logging.info(f"✅ Successfully imported '{tile_file_name}'.")
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
    
    The filename is generated dynamically from the wall assembly.
    After exporting, the export timestamp is updated in the metadata.
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

        update_last_export(wall_assembly.name, datetime.now().isoformat())
    except Exception as e:
        logging.error(f"❌ ERROR: Failed to export wall: {e}")

if __name__ == "__main__":
    generate_flemish_wall()
