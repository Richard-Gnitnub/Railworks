import cadquery as cq

def replicate_corner_by_mirror(corner: cq.Workplane, mirror_plane: str = "YZ", translation: list = None) -> cq.Workplane:
    """
    Replicates a corner by mirroring it along a specified plane and applying an optional translation.
    
    :param corner: The CadQuery solid representing the corner.
    :param mirror_plane: The mirror plane ("XY", "YZ", or "XZ"). For example, "YZ" mirrors across the X=0 plane.
    :param translation: Optional translation vector [x, y, z] to apply after mirroring.
    :return: The mirrored (and optionally translated) corner.
    """
    if mirror_plane.upper() == "YZ":
        mirrored = corner.mirror("YZ")
    elif mirror_plane.upper() == "XZ":
        mirrored = corner.mirror("XZ")
    elif mirror_plane.upper() == "XY":
        mirrored = corner.mirror("XY")
    else:
        raise ValueError(f"Invalid mirror plane: {mirror_plane}. Must be 'XY', 'YZ', or 'XZ'.")
    
    if translation:
        mirrored = mirrored.translate(tuple(translation))
    return mirrored
