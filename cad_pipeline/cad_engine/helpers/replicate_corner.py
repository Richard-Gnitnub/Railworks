import cadquery as cq
import logging
from cad_pipeline.cad_engine.globals.error_handler import log_error

def replicate_corner_by_mirror(corner: cq.Workplane, mirror_plane: str = "YZ", translation: list = None) -> cq.Workplane:
    """
    Replicates a corner by mirroring it along a specified plane and applying an optional translation.
    
    :param corner: The CadQuery solid representing the corner.
    :param mirror_plane: The mirror plane ("XY", "YZ", or "XZ"). For example, "YZ" mirrors across the X=0 plane.
    :param translation: Optional translation vector [x, y, z] to apply after mirroring.
    :return: The mirrored (and optionally translated) corner.
    """
    logging.debug(f"Replicating corner with mirror_plane: {mirror_plane} and translation: {translation}")
    try:
        if mirror_plane.upper() == "YZ":
            mirrored = corner.mirror("YZ")
        elif mirror_plane.upper() == "XZ":
            mirrored = corner.mirror("XZ")
        elif mirror_plane.upper() == "XY":
            mirrored = corner.mirror("XY")
        else:
            msg = f"Invalid mirror plane: {mirror_plane}. Must be 'XY', 'YZ', or 'XZ'."
            log_error(msg)
            raise ValueError(msg)
        
        if translation:
            mirrored = mirrored.translate(tuple(translation))
        logging.debug("Corner replication successful.")
        return mirrored
    except Exception as e:
        log_error("Error in replicate_corner_by_mirror", e)
        raise
