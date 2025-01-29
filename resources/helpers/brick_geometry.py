"""
brick_geometry.py - Handles brick creation logic.
"""

import cadquery as cq

def create_full_brick(config):
    """Creates a full-sized brick with chamfered edges to simulate mortar."""
    return (
        cq.Workplane("XY")
        .box(config["brick_length"], config["brick_width"], config["brick_height"])
        .edges("|Z or |X")
        .chamfer(config["mortar_chamfer"])
    )

def create_half_brick(config):
    """Creates a half-sized brick with chamfered edges to simulate mortar."""
    return (
        cq.Workplane("XY")
        .box(config["brick_length"] / 2, config["brick_width"], config["brick_height"])
        .edges("|Z or |X")
        .chamfer(config["mortar_chamfer"])
    )
