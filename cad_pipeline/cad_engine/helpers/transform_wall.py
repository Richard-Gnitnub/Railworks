import cadquery as cq

def transform_wall(wall, rotation_angle, translation_vector):
    """
    Applies rotation and translation to a wall.

    :param wall: The CadQuery wall solid.
    :param rotation_angle: Rotation angle in degrees (around the Z-axis).
    :param translation_vector: Translation vector as a list or tuple [x, y, z].
    :return: The transformed wall.
    """
    transformed = wall.rotate((0, 0, 1), (0, 0, 0), rotation_angle)
    return transformed.translate(tuple(translation_vector))
