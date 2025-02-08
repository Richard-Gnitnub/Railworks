import cadquery as cq

def generate_fence(parameters):
    """
    Generates a simple wooden fence.
    """
    width = parameters.get("width", 2500)
    height = parameters.get("height", 1800)
    slat_spacing = parameters.get("slat_spacing", 50)

    fence = cq.Workplane("XY")
    num_slats = int(width / slat_spacing)

    for i in range(num_slats):
        slat = cq.Workplane("XY").box(50, height, 20).translate((i * slat_spacing, 0, 0))
        fence = fence.union(slat)

    return fence
