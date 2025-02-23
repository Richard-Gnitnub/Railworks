import cadquery as cq
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def create_cutout_shape(width: float, height: float, depth: float) -> cq.Workplane:
    """
    Creates a rectangular cutout shape.
    """
    return cq.Workplane("XY").rect(width, height).extrude(depth)

def apply_cutouts(wall: cq.Workplane, cutouts: list) -> cq.Workplane:
    """
    Applies manually defined cutouts to a wall model.
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
            shape = create_cutout_shape(width, height, depth)
            wall = wall.cut(shape.translate((x, 0, z)))
        except KeyError as e:
            logging.error(f"❌ ERROR: Missing required key in cutout definition: {e}")
            continue

    logging.info("✅ All cutouts applied successfully.")
    return wall


# ---------------------------------------------
# New functions for a pitched (gable-like) cut
# ---------------------------------------------

def create_pitched_cut_shape(width: float, eave_height: float, apex_height: float, thickness: float) -> cq.Workplane:
    """
    Creates a pitched cut shape that can be subtracted from a wall 
    to form a gable-like top. The shape is essentially a triangular wedge.
    
    :param width: Horizontal width of the gable end.
    :param eave_height: The lower edge height.
    :param apex_height: The peak of the gable (above the eave).
    :param thickness: The thickness in the wall's extrusion direction.
    :return: A CadQuery Workplane object representing the wedge cut.
    """
    try:
        # We'll create a 2D triangular profile in the XY plane, 
        # then extrude in Z or Y (depending on your coordinate system).
        
        wedge_profile = (
            cq.Workplane("XY")
            # Draw a polyline for a triangle from (0,0) to (width,0) to the apex, then close
            .polyline([
                (0, 0),
                (width, 0),
                (width/2, apex_height),  # apex is apex_height above the eave
                (0, 0)
            ])
            .close()
        )

        # Translate it up by eave_height if you want the wedge to start at the eave
        wedge_profile = wedge_profile.translate((0, eave_height, 0))

        # Extrude the wedge by 'thickness' along the Y or Z axis as needed
        # Adjust as necessary to match your wall orientation
        wedge_solid = wedge_profile.extrude(thickness)

        return wedge_solid
    except Exception as e:
        logging.error(f"❌ Error creating pitched cut shape: {e}")
        return cq.Workplane("XY")  # Return an empty shape on failure

def apply_pitched_cut(wall: cq.Workplane, pitch_params: dict) -> cq.Workplane:
    """
    Applies a pitched (gable-like) cut to the top of a wall model.
    
    :param wall: The base wall CadQuery object.
    :param pitch_params: Dict with keys: 'width', 'eave_height', 'apex_height', 'thickness',
                        plus optional 'x_offset' or 'z_offset' to position the wedge.
    :return: Modified wall model with the pitched cut.
    """
    try:
        width        = pitch_params["width"]
        eave_height  = pitch_params["eave_height"]
        apex_height  = pitch_params["apex_height"]
        thickness    = pitch_params["thickness"]
        x_offset     = pitch_params.get("x_offset", 0)
        z_offset     = pitch_params.get("z_offset", 0)

        wedge = create_pitched_cut_shape(width, eave_height, apex_height, thickness)
        # Position the wedge as needed
        wedge = wedge.translate((x_offset, 0, z_offset))

        logging.info(f"🛠 Applying pitched cut: width={width}, eave_height={eave_height}, apex_height={apex_height}, thickness={thickness}")
        wall = wall.cut(wedge)
        logging.info("✅ Pitched cut applied successfully.")
    except KeyError as e:
        logging.error(f"❌ Missing required key in pitched cut parameters: {e}")
    except Exception as e:
        logging.error(f"❌ Error applying pitched cut: {e}")
    return wall
