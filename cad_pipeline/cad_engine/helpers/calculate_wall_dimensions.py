import logging
from datetime import datetime
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.globals.metadata_handler import update_assembly_metadata

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def calculate_wall_dimensions() -> dict:
    """
    Calculates wall dimensions from brick geometry and tile parameters, taking into account
    the selected brick pattern. It retrieves parameters from the "brick_geometry" and 
    "flemish_brick_tile_generator" assemblies, then calculates the wall width, height, and depth.
    
    The brick pattern is logged for informational purposes.
    
    The calculated dimensions are stored as metadata in the "flemish_wall_generator" assembly,
    along with a timestamp.
    
    Returns:
        dict: A dictionary with keys 'width', 'height', and 'depth'.
    """
    logging.info("Starting wall dimension calculation.")
    try:
        brick_assembly = Assembly.objects.get(name="brick_geometry")
        logging.info("Retrieved brick geometry assembly.")
        tile_assembly  = Assembly.objects.get(name="flemish_brick_tile_generator")
        logging.info("Retrieved tile generator assembly.")
    except Exception as e:
        logging.error(f"Error retrieving assemblies: {e}")
        return None

    brick_params = brick_assembly.parameters
    tile_params  = tile_assembly.parameters

    try:
        brick_length   = brick_params["brick_length"]    # e.g., 215 mm
        brick_height   = brick_params["brick_height"]    # e.g., 65 mm
        tile_width     = tile_params["tile_width"]         # e.g., 5 bricks
        row_repetition = tile_params["row_repetition"]     # e.g., 10 rows
        bond_pattern   = tile_params.get("bond_pattern", "default")
        logging.info("Retrieved all necessary parameters for calculation.")
    except KeyError as e:
        logging.error(f"Missing required parameter: {e}")
        return None

    wall_width  = brick_length * tile_width
    wall_height = brick_height * row_repetition
    wall_depth  = tile_params.get("wall_depth", 300)

    logging.debug(f"Basic dimensions - Width: {wall_width}, Height: {wall_height}, Depth: {wall_depth}")

    # Log the brick pattern being used.
    if bond_pattern.lower() == "flemish":
        logging.info("Using Flemish bond pattern.")
    elif bond_pattern.lower() == "stretcher":
        logging.info("Using Stretcher bond pattern.")
    elif bond_pattern.lower() == "stack":
        logging.info("Using Stack bond pattern.")
    else:
        logging.info(f"Using default brick pattern: {bond_pattern}")

    dimensions = {"width": wall_width, "height": wall_height, "depth": wall_depth}
    logging.info(f"Calculated wall dimensions: {dimensions}")

    # Update metadata with the computed dimensions and a timestamp.
    metadata_update = {
        "computed_dimensions": dimensions,
        "timestamp": datetime.now().isoformat()
    }
    if update_assembly_metadata("flemish_wall_generator", metadata_update):
        logging.info("Metadata updated successfully in the wall generator assembly.")
    else:
        logging.error("Failed to update metadata in the wall generator assembly.")

    logging.info("✅ Wall dimension calculation completed.")
    return dimensions
