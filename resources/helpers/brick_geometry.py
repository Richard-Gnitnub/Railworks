"""
brick_geometry.py - Handles all geometry-related operations for brick tiles.
"""

import cadquery as cq


def create_full_brick(config):
    """
    Creates a full-sized brick with chamfered edges to simulate mortar.
    :param config: Dictionary containing tile configuration values.
    """
    return (
        cq.Workplane("XY")
        .box(config["brick_length"], config["brick_width"], config["brick_height"])
        .edges("|Z or |X")  # Apply chamfer to vertical edges
        .chamfer(config["mortar_chamfer"])
        .translate((config["brick_length"] / 2, config["brick_width"] / 2, config["brick_height"] / 2))
    )


def create_half_brick(config):
    """
    Creates a half-sized brick with chamfered edges.
    :param config: Dictionary containing tile configuration values.
    """
    return (
        cq.Workplane("XY")
        .box(config["brick_length"] / 2, config["brick_width"], config["brick_height"])
        .edges("|Z or |X")  # Apply chamfer
        .chamfer(config["mortar_chamfer"])
        .translate((config["brick_length"] / 4, config["brick_width"] / 2, config["brick_height"] / 2))
    )
