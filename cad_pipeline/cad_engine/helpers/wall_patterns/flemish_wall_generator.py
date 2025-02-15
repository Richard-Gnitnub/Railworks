import logging
import cadquery as cq
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.helpers.tile_patterns.flemish_brick_tile_generator import generate_flemish_brick_tile
from ocp_vscode import show_object

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def generate_flemish_wall():
    """
    Generates a Flemish Bond Brick Wall by assembling multiple pre-generated tile segments.
    """
    logging.info("🚀 Starting Flemish Brick Wall Assembly...")

    # ✅ **Step 1: Retrieve Wall Parameters**
    try:
        wall_assembly = Assembly.objects.get(name="flemish_wall")
    except Assembly.DoesNotExist:
        logging.error("❌ ERROR: Flemish Wall MPTT node not found. Ensure database is set up correctly.")
        return

    wall_params = wall_assembly.parameters
    wall_width = wall_params.get("wall_width", 4)  # Number of tiles wide
    wall_height = wall_params.get("wall_height", 3)  # Number of tiles high

    logging.info(f"✅ Wall Parameters: Width={wall_width} tiles, Height={wall_height} tiles")

    # ✅ **Step 2: Create an Empty Workplane for the Wall**
    wall_model = cq.Workplane("XY")

    # ✅ **Step 3: Generate & Place Tiles into the Wall**
    for row in range(wall_height):
        for col in range(wall_width):
            logging.info(f"🔹 Placing tile at Row {row + 1}, Column {col + 1}")

            # Generate a Flemish Brick Tile (already follows Flemish bond logic)
            tile_model = generate_flemish_brick_tile()

            if tile_model:
                x_offset = col * 430  # Tile width (adjust if needed)
                z_offset = row * 130  # Tile height (adjust if needed)

                logging.info(f"📏 Placing tile at (X={x_offset}, Z={z_offset})")

                # Add tile to the wall at the correct position
                wall_model = wall_model.union(tile_model.translate((x_offset, 0, z_offset)))

    # ✅ **Step 4: Visualize the Assembled Wall**
    logging.info("🎨 Displaying Flemish Wall in Viewer...")
    show_object(wall_model, name="Flemish Wall")

    logging.info("✅ Flemish Wall Assembly Complete!")
    return wall_model
