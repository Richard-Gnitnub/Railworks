from cad_pipeline.models.assembly import Assembly
import cadquery as cq
from cad_pipeline.cad_engine.helpers.brick_geometry import (
    create_full_brick_aligned, create_half_brick_aligned
)

def assemble_brick_tile(tile: Assembly, brick_parameters_list: list) -> cq.Workplane:
    """
    Assembles a brick tile using CadQuery's context solid behavior.
    Supports: Flemish, Stretcher, Stack Bond.
    """
    print("\n🔎 DEBUG: Starting `assemble_brick_tile` function...\n")

    # Validate inputs
    if not isinstance(tile, Assembly):
        raise ValueError(f"❌ Expected an Assembly object for the tile, but got {type(tile)}")
    if not isinstance(brick_parameters_list, list):
        raise ValueError(f"❌ Expected a list of brick parameters, but got {type(brick_parameters_list)}")
    if not brick_parameters_list:
        raise ValueError("❌ Brick parameters list is empty. Ensure bricks are correctly assigned.")

    # Retrieve tile parameters
    tile_config = tile.parameters
    bond_pattern = tile_config.get("bond_pattern", "flemish")
    row_repetition = tile_config.get("row_repetition", 2)
    tile_width = tile_config.get("tile_width", 4)

    print(f"✅ Tile Configuration: {tile_config}")
    print(f"✅ Bond Pattern: {bond_pattern}, Row Repetition: {row_repetition}, Tile Width: {tile_width}")

    # Start with an empty Workplane
    tile_workplane = cq.Workplane("XY")

    # Assemble rows
    for i in range(row_repetition):
        print(f"\n🔹 DEBUG: Creating row {i + 1}/{row_repetition}")

        row_x_offset = 0
        if bond_pattern == "flemish" and i % 2 != 0:
            row_x_offset = -brick_parameters_list[0]["brick_length"] / 1.5  # Align half-brick centre

        x_offset = row_x_offset
        z_offset = i * brick_parameters_list[0]["brick_height"]

        for j in range(tile_width):
            brick_params = brick_parameters_list[j % len(brick_parameters_list)]
            print(f"🔸 DEBUG: Using brick {j + 1}/{tile_width} with parameters: {brick_params}")

            # Create the appropriate brick model using `brick_geometry.py`
            if bond_pattern == "flemish":
                brick_model = (
                    create_half_brick_aligned(**brick_params) if j % 2 else create_full_brick_aligned(**brick_params)
                )
                print(f"✅ Adding {'Half' if j % 2 else 'Full'} Brick at x_offset {x_offset}")

            elif bond_pattern == "stretcher":
                brick_model = create_full_brick_aligned(**brick_params)
                print(f"✅ Adding Stretcher Bond Brick at x_offset {x_offset}")

            elif bond_pattern == "stack":
                brick_model = create_full_brick_aligned(**brick_params)
                print(f"✅ Adding Stack Bond Brick at x_offset {x_offset}")

            else:
                raise ValueError(f"❌ Unsupported bond pattern: {bond_pattern}")

            # Use CadQuery's context solid behavior to combine bricks
            tile_workplane = tile_workplane.union(brick_model.translate((x_offset, 0, z_offset)))
            x_offset += brick_params["brick_length"] / (2 if j % 2 else 1)

        print(f"🔹 Row {i + 1} completed at z_offset {z_offset}")

    print("\n✅ DEBUG: Tile Assembly Completed!\n")
    return tile_workplane