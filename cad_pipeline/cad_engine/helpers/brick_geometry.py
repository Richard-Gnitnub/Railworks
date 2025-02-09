from functools import lru_cache
import cadquery as cq

@lru_cache(maxsize=None)
def create_full_brick_aligned(**params):
    """Creates and caches a full-sized brick with chamfered edges."""
    # Debugging log
    print(f"Debug: Parameters in create_full_brick_aligned: {params}")

    length = params["brick_length"]
    width = params["brick_width"]
    height = params["brick_height"]
    chamfer = params["mortar_chamfer"]

    brick = (
        cq.Workplane("XY")
        .box(length, width, height)
        .edges("|Z or |X")
        .chamfer(chamfer)
    )
    return brick.translate((length / 2, width / 2, height / 2))

@lru_cache(maxsize=None)
def create_half_brick_aligned(**params):
    """Creates and caches a half-sized brick with chamfered edges."""
    # Debugging log
    print(f"Debug: Parameters in create_half_brick_aligned: {params}")

    length = params["brick_length"] / 2
    width = params["brick_width"]
    height = params["brick_height"]
    chamfer = params["mortar_chamfer"]

    brick = (
        cq.Workplane("XY")
        .box(length, width, height)
        .edges("|Z or |X")
        .chamfer(chamfer)
    )
    return brick.translate((length / 2, width / 2, height / 2))
