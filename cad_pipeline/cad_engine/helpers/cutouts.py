import cadquery as cq
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def create_cutout_shape(width: float, height: float, depth: float) -> cq.Workplane:
    """
    Creates a rectangular cutout shape.
    
    :param width: Width of the cutout.
    :param height: Height of the cutout.
    :param depth: Depth to extrude the cutout.
    :return: A CadQuery Workplane object representing the cutout.
    """
    return cq.Workplane("XY").rect(width, height).extrude(depth)

def apply_cutouts(wall: cq.Workplane, cutouts: list) -> cq.Workplane:
    """
    Applies manually defined cutouts to a wall model.
    
    :param wall: The base wall CadQuery object.
    :param cutouts: List of dictionaries each with keys 'x', 'z', 'width', 'height', and 'depth'.
    :return: Modified wall model with applied cutouts.
    """
    if not cutouts:
        logging.warning("⚠️ No cutout data provided. Skipping cutout application.")
        return wall

    for cutout in cutouts:
        try:
            x = cutout["x"]
            z = cutout["z"]
            width = cutout["width"]
            height = cutout["height"]
            depth = cutout["depth"]

            logging.info(f"🛠 Applying cutout at X={x}, Z={z}, Size=({width}, {height}), Depth={depth}")

            # Create and position the cutout shape
            shape = create_cutout_shape(width, height, depth)
            wall = wall.cut(shape.translate((x, 0, z)))
        except KeyError as e:
            logging.error(f"❌ ERROR: Missing required key in cutout definition: {e}")
            continue

    logging.info("✅ All cutouts applied successfully.")
    return wall
