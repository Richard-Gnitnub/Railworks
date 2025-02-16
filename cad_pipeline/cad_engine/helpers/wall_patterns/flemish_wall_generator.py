import logging
import cadquery as cq
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.globals.import_handler import import_step_subassembly
from cad_pipeline.cad_engine.helpers.tile_patterns.flemish_brick_tile_generator import generate_flemish_brick_tile
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from cad_pipeline.cad_engine.helpers.cutouts import apply_cutout
from ocp_vscode import show_object

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def generate_flemish_wall():
    """
    Generates a Flemish Brick Wall by:
    - Importing an existing wall STEP file from the database.
    - Triggering a tile rebuild if no STEP file exists.
    - Applying cutouts dynamically based on stored JSON parameters.
    - Exporting the final wall with modifications.
    """
    logging.info("🚀 Starting Flemish Brick Wall Assembly...")

    # ✅ **Step 1: Retrieve Wall Parameters from Assembly**
    try:
        wall_assembly = Assembly.objects.get(name="generate_flemish_wall")
    except Assembly.DoesNotExist:
        logging.error("❌ ERROR: Wall assembly record not found.")
        return

    # ✅ **Ensure Cutout Parameters Exist (No Defaults)**
    if "cutouts" not in wall_assembly.parameters or not isinstance(wall_assembly.parameters["cutouts"], list):
        logging.error("❌ ERROR: Missing or invalid `cutouts` parameter in wall configuration.")
        return

    cutouts = wall_assembly.parameters["cutouts"]
    logging.info(f"📏 Retrieved {len(cutouts)} cutout(s) from database.")

    # ✅ **Step 2: Import or Generate Tile Assembly**
    tile_file_name = "generate_flemish_brick_tile.step"
    tile_model = import_step_subassembly(tile_file_name, generator_function=generate_flemish_brick_tile)

    if tile_model is None:
        logging.error("❌ Failed to import or generate tile. Cannot proceed.")
        return

    logging.info(f"✅ Successfully imported `{tile_file_name}` into the wall assembly.")

    # ✅ **Step 3: Apply Cutouts to the Wall**
    logging.info(f"🛠 Applying cutouts dynamically...")
    wall_with_cutouts = apply_cutout(tile_model, cutouts)

    logging.info("\n✅ Wall Assembly with Cutouts Completed!")

    # ✅ **Step 4: Export Wall Using `export_handler`**
    try:
        export_config = {
            "export_formats": ["step", "stl"],
            "file_name": "flemish_wall",
            "component": wall_assembly
        }
        exported_files = export_assembly(wall_with_cutouts, **export_config)

        logging.info("✅ Wall Export Completed!")
        for fmt, file_data in exported_files.items():
            logging.info(f"   - Exported Format: {fmt.upper()}, Size: {len(file_data.file_data)} bytes")

    except Exception as e:
        logging.error(f"❌ ERROR: Failed to export wall: {e}")
        return

    # ✅ **Step 5: Display Wall**
    show_object(wall_with_cutouts, name="Flemish Wall")

    return wall_with_cutouts
