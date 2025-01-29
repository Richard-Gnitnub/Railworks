"""
tile_assembly.py - Assembles full tile structures dynamically.
"""

import cadquery as cq
from resources.helpers.brick_helpers import assemble_brick_row

def assemble_tile(config):
    """
    Assembles a full tile using the selected tile type.
    """
    tile_type = config["tile_type"]
    tile_assembly = cq.Assembly()
    
    if tile_type == "bricks":
        for i in range(config["row_repetition"]):
            row_assembly = assemble_brick_row(config, i)
            z_offset = i * config["brick_height"]
            tile_assembly.add(row_assembly, loc=cq.Location(cq.Vector(0, 0, z_offset)))
    else:
        raise ValueError(f"Unsupported tile type: {tile_type}")

    return tile_assembly
