"""
brick_helpers.py - Handles assembling bricks into rows.
"""

import cadquery as cq
from resources.helpers.brick_geometry import create_full_brick, create_half_brick

def assemble_brick_row(config, row_index):
    """
    Assembles a single row of bricks based on the specified bond pattern.
    """
    row_assembly = cq.Assembly()
    full_brick = create_full_brick(config)
    half_brick = create_half_brick(config)
    
    bond_pattern = config.get("bond_pattern", "flemish")
    tile_width = config["tile_width"]
    
    # Determine row shift for proper alignment
    row_x_offset = (-config["brick_length"] / 2) if row_index % 2 != 0 and bond_pattern == "flemish" else 0
    x_offset = row_x_offset

    for j in range(tile_width):
        if bond_pattern in ["flemish", "stretcher"]:
            if j % 2 == 0:
                row_assembly.add(full_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)))
                x_offset += config["brick_length"]
            else:
                row_assembly.add(half_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)))
                x_offset += config["brick_length"] / 2
        elif bond_pattern == "stack":
            row_assembly.add(full_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)))
            x_offset += config["brick_length"]

    return row_assembly
