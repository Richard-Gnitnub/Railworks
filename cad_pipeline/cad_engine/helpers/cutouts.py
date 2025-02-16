import cadquery as cq
import logging

# ✅ Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def apply_cutout(wall: cq.Workplane, cutouts: list):
    """
    Applies multiple rectangular cutouts to a given wall model.

    :param wall: The base wall CadQuery object.
    :param cutouts: List of cutouts, each containing {"x", "z", "width", "height", "depth"}.
    :return: Modified wall model with cutouts.
    """
    if not cutouts:
        logging.warning("⚠️ No cutout data provided. Skipping cutout application.")
        return wall

    for cutout in cutouts:
        try:
            # ✅ Extract cutout parameters dynamically
            x, z = cutout["x"], cutout["z"]
            cut_width, cut_height, cut_depth = cutout["width"], cutout["height"], cutout["depth"]

            logging.info(f"🛠 Applying cutout at X={x}, Z={z}, Size=({cut_width}, {cut_height}), Depth={cut_depth}")

            # ✅ Apply cutout dynamically using JSON data
            cutout_shape = cq.Workplane("XY").rect(cut_width, cut_height).extrude(cut_depth)
            wall = wall.cut(cutout_shape.translate((x, 0, z)))

        except KeyError as e:
            logging.error(f"❌ ERROR: Missing required key in cutout definition: {e}")
            continue

    logging.info("✅ All cutouts applied successfully.")
    return wall
