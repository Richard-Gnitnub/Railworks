import logging
import cadquery as cq
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.models.exported_file import ExportedFile
from cad_pipeline.cad_engine.helpers.tile_patterns.flemish_brick_tile_generator import generate_flemish_brick_tile
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from ocp_vscode import show_object

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def generate_flemish_wall():
    """
    Generates a Flemish Brick Wall assembly by importing an existing STEP file of the tile
    or regenerating if not found. Uses export_handler for file exports.
    """
    logging.info("🚀 Starting Flemish Brick Wall Assembly...")

    # ✅ **Step 1: Retrieve Wall Parameters**
    try:
        wall_assembly = Assembly.objects.get(name="generate_flemish_wall")
    except Assembly.DoesNotExist:
        logging.error("❌ ERROR: Wall assembly record not found.")
        return

    wall_params = wall_assembly.parameters
    required_wall_params = ["wall_width", "wall_height"]

    missing_wall_keys = [k for k in required_wall_params if k not in wall_params]
    if missing_wall_keys:
        logging.error(f"❌ ERROR: Missing required wall parameters: {missing_wall_keys}")
        return

    wall_width = wall_params["wall_width"]  # Number of tiles across
    wall_height = wall_params["wall_height"]  # Number of tiles high

    logging.info(f"📏 Wall Grid: {wall_width} x {wall_height}")

    # ✅ **Step 2: Check for Existing Tile STEP File**
    tile_filename = "generate_flemish_brick_tile.step"
    tile_file = ExportedFile.objects.filter(file_name=tile_filename, file_format="step").order_by("-created_at").first()

    if tile_file:
        logging.info(f"✅ Found existing tile STEP file: {tile_filename}, Importing...")
        tile_model = cq.importers.importStep(tile_file.file_data)
    else:
        logging.warning(f"⚠️ Tile STEP file missing, regenerating tile...")
        tile_model = generate_flemish_brick_tile()
        if tile_model is None:
            logging.error("❌ Tile generation failed. Cannot build wall.")
            return

    # ✅ **Step 3: Retrieve Tile Dimensions**
    tile_bb = tile_model.val().BoundingBox()
    tile_width = tile_bb.xlen  # Dynamic width from the bounding box
    tile_height = tile_bb.zlen  # Dynamic height from the bounding box

    logging.info(f"📏 Tile Dimensions: {tile_width} x {tile_height}")

    # ✅ **Step 4: Initialize Wall Model**
    wall_model = cq.Workplane("XY")

    # ✅ Uniform grid placement (NO staggering)
    for row in range(wall_height):
        for col in range(wall_width):
            x_offset = col * tile_width
            z_offset = row * tile_height

            logging.info(f"🔹 Placing tile at Row {row+1}, Column {col+1} at (X={x_offset}, Z={z_offset})")

            translated_tile = tile_model.translate((x_offset, 0, z_offset))  # Ensure this returns a new object
            wall_model = wall_model.union(translated_tile)

    logging.info("\n✅ Wall Assembly Completed!")

    # ✅ **Step 6: Export Wall Using `export_handler`**
    try:
        export_config = {
            "export_formats": ["step", "stl"],
            "file_name": "flemish_wall",
            "component": wall_assembly
        }
        exported_files = export_assembly(wall_model, **export_config)

        logging.info("✅ Wall Export Completed!")
        for fmt in ["step", "stl"]:  # Ensure no missing keys
            file_data = exported_files.get(fmt)
            if file_data:
                logging.info(f"   - Exported Format: {fmt.upper()}, Size: {len(file_data.file_data)} bytes")

    except Exception as e:
        logging.error(f"❌ ERROR: Failed to export wall: {e}")
        return

    # ✅ **Step 7: Display Wall**
    show_object(wall_model, name="Flemish Wall")

    return wall_model
