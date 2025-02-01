import cadquery as cq
from functools import lru_cache

def config_to_tuple(config):
    """Converts a configuration dictionary into a sorted, immutable tuple."""
    return tuple((k, tuple(v) if isinstance(v, list) else v) for k, v in sorted(config.items()))

@lru_cache(maxsize=None)
def create_full_brick_aligned(config_tuple):
    """Creates and caches a full-sized brick with chamfered edges."""
    config = dict(config_tuple)  # Convert tuple back to dictionary

    # Debugging log
    print(f"Debug: Config restored in create_full_brick_aligned: {config}")

    length = config["brick_length"]
    width = config["brick_width"]
    height = config["brick_height"]
    chamfer = config["mortar_chamfer"]

    brick = (
        cq.Workplane("XY")
        .box(length, width, height)
        .edges("|Z or |X")
        .chamfer(chamfer)
    )
    return brick.translate((length / 2, width / 2, height / 2))

@lru_cache(maxsize=None)
def create_half_brick_aligned(config_tuple):
    """Creates and caches a half-sized brick with chamfered edges."""
    config = dict(config_tuple)  # Convert tuple back to dictionary

    # Debugging log
    print(f"Debug: Config restored in create_half_brick_aligned: {config}")

    length = config["brick_length"] / 2
    width = config["brick_width"]
    height = config["brick_height"]
    chamfer = config["mortar_chamfer"]

    brick = (
        cq.Workplane("XY")
        .box(length, width, height)
        .edges("|Z or |X")
        .chamfer(chamfer)
    )
    return brick.translate((length / 2, width / 2, height / 2))
