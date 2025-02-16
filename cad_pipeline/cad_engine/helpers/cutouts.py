import cadquery as cq
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def apply_cutout(wall: cq.Workplane, cutout_grid: list):
    """
    Applies cutouts to a given wall model using grid-based cutout positions.
    
    :param wall: The base wall CadQuery object.
    :param cutout_grid: List of cutout positions dynamically generated.
    :return: Modified wall model with applied cutouts.
    """
    if not cutout_grid:
        logging.warning("⚠️ No cutout data provided. Skipping cutout application.")
        return wall

    for cutout in cutout_grid:
        try:
            x, z = cutout["x"], cutout["z"]
            cut_width = cutout["width"]
            cut_height = cutout["height"]
            cut_depth = cutout["depth"]

            logging.info(f"🛠 Applying cutout at X={x}, Z={z}, Size=({cut_width}, {cut_height}), Depth={cut_depth}")

            # Create and position the cutout shape
            cutout_shape = cq.Workplane("XY").rect(cut_width, cut_height).extrude(cut_depth)
            wall = wall.cut(cutout_shape.translate((x, 0, z)))
        except KeyError as e:
            logging.error(f"❌ ERROR: Missing required key in cutout definition: {e}")
            continue

    logging.info("✅ All cutouts applied successfully.")
    return wall
