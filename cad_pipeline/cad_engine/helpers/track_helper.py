import cadquery as cq

def generate_track(parameters):
    """
    Generates a railway track based on parameters.
    """
    length = parameters.get("length", 1000)
    rail_height = parameters.get("rail_height", 120)
    sleeper_spacing = parameters.get("sleeper_spacing", 500)

    track = cq.Workplane("XY")

    num_sleepers = int(length / sleeper_spacing)

    for i in range(num_sleepers):
        sleeper = cq.Workplane("XY").box(250, 50, 20).translate((i * sleeper_spacing, 0, 0))
        track = track.union(sleeper)

    return track
