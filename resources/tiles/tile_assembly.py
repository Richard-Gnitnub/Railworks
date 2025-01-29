"""
tile_assembly.py - Handles row placement logic for different brick bond patterns.
"""

import cadquery as cq
from resources.helpers.brick_geometry import create_full_brick, create_half_brick

def assemble_tile(config):
    """
    Creates a tile assembly dynamically based on the YAML configuration.
    Supports multiple bond patterns like 'flemish', 'stretcher', 'stack'.
    """
    tile_type = config["tile_type"]
    bond_pattern = config.get("bond_pattern", "flemish")  # Default to Flemish
    tile_assembly = cq.Assembly()
    
    row_repetition = config["row_repetition"]
    tile_width = config["tile_width"]
    offset_X = config.get("offset_X", 0)

    for i in range(row_repetition):
        row_assembly = cq.Assembly()
        half_brick = create_half_brick(config)
        full_brick = create_full_brick(config)

        # Apply Bond Pattern Logic
        if bond_pattern == "flemish":
            row_x_offset = (-config["brick_length"] / 2) if i % 2 != 0 else 0
        elif bond_pattern == "stretcher":
            row_x_offset = 0  # All rows aligned
        elif bond_pattern == "stack":
            row_x_offset = 0  # Stack Bond has aligned rows
        else:
            raise ValueError(f"Unsupported bond pattern: {bond_pattern}")

        x_offset = row_x_offset

        for j in range(tile_width):
            if bond_pattern == "flemish":
                if j % 2 == 0:
                    row_assembly.add(full_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)), name=f"Full Brick Row{i}-Col{j}")
                    x_offset += config["brick_length"]
                else:
                    row_assembly.add(half_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)), name=f"Half Brick Row{i}-Col{j}")
                    x_offset += config["brick_length"] / 2
            elif bond_pattern == "stretcher":
                row_assembly.add(full_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)), name=f"Full Brick Row{i}-Col{j}")
                x_offset += config["brick_length"]
            elif bond_pattern == "stack":
                row_assembly.add(full_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)), name=f"Stacked Brick Row{i}-Col{j}")
                x_offset += config["brick_length"]

        # Apply Z-offset for vertical stacking
        z_offset = i * config["brick_height"]
        tile_assembly.add(row_assembly, loc=cq.Location(cq.Vector(offset_X * i, 0, z_offset)), name=f"Row {i}")

    return tile_assembly
