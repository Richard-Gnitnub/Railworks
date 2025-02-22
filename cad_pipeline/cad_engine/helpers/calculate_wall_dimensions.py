import logging
from datetime import datetime
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.globals.metadata_handler import update_computed_dimensions

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def calculate_wall_dimensions() -> dict:
    """
    Calculates wall dimensions from brick geometry and tile parameters, taking into account
    the selected brick pattern.
    
    For a Flemish bond (if tile_width is even), the effective width is calculated as:
    
       wall_width = (tile_width/2 * brick_length) + (tile_width/2 * (brick_length / 2))
    
    Otherwise, it uses:
    
       wall_width = brick_length * tile_width
    
    The wall height is calculated as:
    
       wall_height = brick_height * row_repetition
    
    The wall depth is taken from tile parameters, defaulting to 300 if unspecified.
    
    The computed dimensions are stored in the "flemish_wall_generator" assembly metadata.
    
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
        tile_width     = tile_params["tile_width"]         # e.g., 10 bricks
        row_repetition = tile_params["row_repetition"]     # e.g., 10 rows
        bond_pattern   = tile_params.get("bond_pattern", "default").lower()
        logging.info("Retrieved all necessary parameters for calculation.")
    except KeyError as e:
        logging.error(f"Missing required parameter: {e}")
        return None

    # Calculate wall width based on the bond pattern.
    if bond_pattern == "flemish":
        if tile_width % 2 != 0:
            logging.warning("Tile width is not even; using default calculation for wall width.")
            wall_width = brick_length * tile_width
        else:
            full_bricks = tile_width // 2
            half_bricks = tile_width // 2
            wall_width = full_bricks * brick_length + half_bricks * (brick_length / 2)
            logging.info("Calculated effective wall width for Flemish bond pattern.")
    else:
        wall_width = brick_length * tile_width

    wall_height = brick_height * row_repetition
    wall_depth  = tile_params.get("wall_depth", 300)

    logging.debug(f"Computed dimensions - Width: {wall_width}, Height: {wall_height}, Depth: {wall_depth}")
    
    dimensions = {"width": wall_width, "height": wall_height, "depth": wall_depth}
    logging.info(f"Calculated wall dimensions: {dimensions}")

    # Update metadata for the "flemish_wall_generator" assembly with computed dimensions.
    if update_computed_dimensions("flemish_wall_generator", dimensions):
        logging.info("Computed dimensions updated successfully in metadata.")
    else:
        logging.error("Failed to update computed dimensions in metadata.")

    logging.info("✅ Wall dimension calculation completed.")
    return dimensions
