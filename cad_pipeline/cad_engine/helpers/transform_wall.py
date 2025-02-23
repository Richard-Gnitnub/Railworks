import cadquery as cq
import logging
from cad_pipeline.cad_engine.globals.error_handler import log_error

def transform_wall(wall, rotation_angle, translation_vector):
    """
    Applies rotation and translation to a wall.

    :param wall: The CadQuery wall solid.
    :param rotation_angle: Rotation angle in degrees (around the Z-axis).
    :param translation_vector: Translation vector as a list or tuple [x, y, z].
    :return: The transformed wall.
    """
    logging.debug(f"Transforming wall: rotating by {rotation_angle} degrees and translating by {translation_vector}")
    try:
        transformed = wall.rotate((0, 0, 1), (0, 0, 0), rotation_angle)
        transformed = transformed.translate(tuple(translation_vector))
        logging.debug("Transformation successful.")
        return transformed
    except Exception as e:
        log_error("Error in transform_wall", e)
        raise
