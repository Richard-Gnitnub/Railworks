import logging
import cadquery as cq
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.helpers.assemble_brick_tile import assemble_brick_tile
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from ocp_vscode import show_object

# ✅ Configure Logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def generate_flemish_brick_tile():
    """
    Generates a Flemish Brick Tile, ensuring:
    - Required assemblies exist.
    - Tile is assembled with correct parameters.
    - Model is exported via `export_assembly()`.
    """
    logging.info("🚀 Starting Flemish Brick Tile Assembly & Export...")

    # ✅ Retrieve or Create Required Assemblies (Ensure Correct Naming)
    try:
        tile_assembly, _ = Assembly.objects.get_or_create(name="flemish_brick_tile_generator")
        brick_geometry, _ = Assembly.objects.get_or_create(name="brick_geometry")
    except Exception as e:
        logging.error(f"❌ ERROR: Database lookup failed: {e}")
        return None

    # ✅ **Validate Required Parameters**
    tile_parameters = tile_assembly.parameters
    brick_parameters = brick_geometry.parameters
    required_tile_params = ["tile_width", "row_repetition", "bond_pattern"]
    required_brick_params = ["brick_length", "brick_width", "brick_height", "mortar_chamfer"]

    missing_tile_keys = [k for k in required_tile_params if k not in tile_parameters]
    missing_brick_keys = [k for k in required_brick_params if k not in brick_parameters]

    if missing_tile_keys or missing_brick_keys:
        logging.error(f"❌ ERROR: Missing required parameters: {missing_tile_keys + missing_brick_keys}")
        return None

    logging.info(f"✅ Tile Parameters: {tile_parameters}")
    logging.info(f"✅ Brick Parameters: {brick_parameters}")

    # ✅ **Generate Tile Model**
    try:
        logging.info("🔧 Generating Tile Model...")
        tile_model = assemble_brick_tile(tile_assembly, [brick_parameters])
        if tile_model is None:
            logging.error("❌ ERROR: `assemble_brick_tile()` returned None! Check input parameters.")
            return None
        logging.info("🧱 Tile Assembly Completed.")
    except Exception as e:
        logging.error(f"❌ ERROR: Failed to assemble brick tile: {e}")
        return None

    # ✅ **Export Using `export_handler.py` (No Manual Filenames)**
    try:
        export_assembly(tile_model, component=tile_assembly)  # ✅ Only passing component!
        logging.info("✅ Tile Export Completed!")
    except Exception as e:
        logging.error(f"❌ ERROR: Failed to export tile: {e}")
        return None

    # ✅ **Visualize Tile**
    logging.info("🎨 Visualizing Tile Model in Viewer...")
    show_object(tile_model, name="Flemish Brick Tile")

    logging.info("✅ Flemish Brick Tile Generation Complete")
    return tile_model
