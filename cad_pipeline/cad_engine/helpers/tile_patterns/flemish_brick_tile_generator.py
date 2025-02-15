import logging
import cadquery as cq
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.helpers.assemble_brick_tile import assemble_brick_tile
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from ocp_vscode import show_object

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def generate_flemish_brick_tile():
    """
    Generates a Flemish Brick Tile, ensures `tile_model` is assigned, and exports it.
    """
    logging.info("🚀 Starting Flemish Brick Tile Assembly & Export Test...")

    # ✅ **Step 1: Retrieve Assembly and Brick Parameters**
    try:
        tile_assembly = Assembly.objects.get(name="generate_flemish_brick_tile")
        brick_geometry = Assembly.objects.get(name="brick_geometry")
    except Assembly.DoesNotExist:
        logging.error("❌ ERROR: Assembly not found. Ensure database records are correct.")
        return

    tile_parameters = tile_assembly.parameters
    brick_parameters = brick_geometry.parameters

    logging.info(f"✅ Tile Parameters: {tile_parameters}")
    logging.info(f"✅ Brick Parameters: {brick_parameters}")

    # ✅ **Ensure Required Parameters Exist**
    required_tile_params = ["tile_width", "row_repetition", "bond_pattern"]
    required_brick_params = ["brick_length", "brick_width", "brick_height", "mortar_chamfer"]

    missing_tile_keys = [k for k in required_tile_params if k not in tile_parameters]
    missing_brick_keys = [k for k in required_brick_params if k not in brick_parameters]

    if missing_tile_keys:
        logging.error(f"❌ ERROR: Missing required tile parameters: {missing_tile_keys}")
        return

    if missing_brick_keys:
        logging.error(f"❌ ERROR: Missing required brick parameters: {missing_brick_keys}")
        return

    # ✅ **Step 2: Generate Tile (Ensure `tile_model` is always assigned)**
    tile_model = None
    try:
        logging.info("🔧 Generating New Tile Model...")
        tile_model = assemble_brick_tile(tile_assembly, [brick_parameters])
        logging.info("🧱 Tile Assembly Completed.")
    except Exception as e:
        logging.error(f"❌ ERROR: Failed to assemble brick tile: {e}")
        return

    # ✅ **Step 3: Ensure `tile_model` is Assigned Before Export**
    if tile_model is None:
        logging.error("❌ ERROR: Tile model was not created. Exiting...")
        return

    # ✅ **Step 4: Export Tile Using `export_handler.py`**
    try:
        export_config = {
            "export_formats": ["step", "stl"],
            "file_name": f"{tile_assembly.name}_export",
            "component": tile_assembly  # ✅ Pass the component for database reference
        }
        exported_files = export_assembly(tile_model, **export_config)

        logging.info("✅ Tile Export Completed!")
        for fmt, file_data in exported_files.items():
            logging.info(f"   - Exported Format: {fmt.upper()}, Size: {len(file_data.file_data)} bytes")

    except Exception as e:
        logging.error(f"❌ ERROR: Failed to export tile: {e}")
        return

    # ✅ **Step 5: Visualize the Tile**
    logging.info("🎨 Displaying Tile in Viewer...")
    show_object(tile_model, name="Brick Tile 1")

    logging.info("✅ Flemish Brick Tile Generation Complete")
