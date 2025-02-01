import cadquery as cq
from resources.helpers.brick_geometry import (
    create_full_brick_aligned, create_half_brick_aligned, config_to_tuple
)

def assemble_brick_tile(config):
    """
    Assembles a brick tile based on the bond pattern defined in YAML.
    Supports: Flemish, Stretcher, Stack Bond.
    """
    config_tuple = config_to_tuple(config)  # ✅ Convert config into a proper tuple
    bond_pattern = config.get("bond_pattern", "flemish")  # Default to Flemish
    offset_X = config.get("offset_X", 0)
    row_repetition = config["row_repetition"]
    tile_width = config["tile_width"]

    tile_assembly = cq.Assembly()

    for i in range(row_repetition):
        row_assembly = cq.Assembly()
        
        print(f"Debug: config_tuple type is {type(config_tuple)}")  # ✅ Debugging
        assert isinstance(config_tuple, tuple), "config_tuple is not a tuple!"  # ✅ Debugging
        
        # ✅ Ensure we pass `config_tuple` as a **tuple**, not a list
        half_brick = create_half_brick_aligned(config_tuple)
        full_brick = create_full_brick_aligned(config_tuple)

        row_x_offset = 0
        if bond_pattern == "flemish" and i % 2 != 0:
            row_x_offset = -config["brick_length"] / 2  # Align half-brick centre

        x_offset = row_x_offset

        for j in range(tile_width):
            if bond_pattern == "flemish":
                if j % 2 == 0:  # 🔹 Add full brick
                    row_assembly.add(full_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)))
                    x_offset += config["brick_length"]
                else:  # 🔹 Add half brick
                    row_assembly.add(half_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)))
                    x_offset += config["brick_length"] / 2

            elif bond_pattern == "stretcher":
                row_assembly.add(full_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)))
                x_offset += config["brick_length"]  # Bricks are aligned in a running bond

            elif bond_pattern == "stack":
                row_assembly.add(full_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)))
                x_offset += config["brick_length"]  # Each brick sits directly above the one below

            else:
                raise ValueError(f"Unsupported bond pattern: {bond_pattern}")

        z_offset = i * config["brick_height"]
        tile_assembly.add(row_assembly, loc=cq.Location(cq.Vector(offset_X * i, 0, z_offset)))

    return tile_assembly
