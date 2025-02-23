import logging
import cadquery as cq
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.helpers.brick_geometry import (
    create_full_brick_aligned, create_half_brick_aligned
)
from cad_pipeline.cad_engine.globals.error_handler import log_error

def assemble_brick_tile(tile: Assembly, brick_parameters_list: list) -> cq.Workplane:
    """
    Assembles a brick tile using CadQuery's context solid behavior.
    Supports: Flemish, Stretcher, Stack Bond.
    """
    logging.debug("🔎 DEBUG: Starting `assemble_brick_tile` function...")

    # Validate inputs
    if not isinstance(tile, Assembly):
        msg = f"Expected an Assembly object for the tile, but got {type(tile)}"
        log_error(msg)
        raise ValueError(msg)
    if not isinstance(brick_parameters_list, list):
        msg = f"Expected a list of brick parameters, but got {type(brick_parameters_list)}"
        log_error(msg)
        raise ValueError(msg)
    if not brick_parameters_list:
        msg = "Brick parameters list is empty. Ensure bricks are correctly assigned."
        log_error(msg)
        raise ValueError(msg)

    # Retrieve tile parameters
    tile_config = tile.parameters
    bond_pattern = tile_config.get("bond_pattern", "flemish")
    row_repetition = tile_config.get("row_repetition", 2)
    tile_width = tile_config.get("tile_width", 4)
    alignment_factor = tile_config.get("alignment_factor", 1.5)

    logging.debug(f"✅ Tile Configuration: {tile_config}")
    logging.debug(f"✅ Bond Pattern: {bond_pattern}, Row Repetition: {row_repetition}, Tile Width: {tile_width}")

    # Start with an empty Workplane
    tile_workplane = cq.Workplane("XY")

    # Assemble rows
    for i in range(row_repetition):
        logging.debug(f"🔹 DEBUG: Creating row {i + 1}/{row_repetition}")

        row_x_offset = 0
        if bond_pattern == "flemish" and i % 2 != 0:
            row_x_offset = -brick_parameters_list[0]["brick_length"] / alignment_factor

        x_offset = row_x_offset
        z_offset = i * brick_parameters_list[0]["brick_height"]

        for j in range(tile_width):
            brick_params = brick_parameters_list[j % len(brick_parameters_list)]
            logging.debug(f"🔸 DEBUG: Using brick {j + 1}/{tile_width} with parameters: {brick_params}")

            # Create the appropriate brick model
            if bond_pattern == "flemish":
                brick_model = (
                    create_half_brick_aligned(**brick_params) if j % 2 else create_full_brick_aligned(**brick_params)
                )
                logging.debug(f"✅ Adding {'Half' if j % 2 else 'Full'} Brick at x_offset {x_offset}")

            elif bond_pattern == "stretcher":
                brick_model = create_full_brick_aligned(**brick_params)
                logging.debug(f"✅ Adding Stretcher Bond Brick at x_offset {x_offset}")

            elif bond_pattern == "stack":
                brick_model = create_full_brick_aligned(**brick_params)
                logging.debug(f"✅ Adding Stack Bond Brick at x_offset {x_offset}")

            else:
                msg = f"Unsupported bond pattern: {bond_pattern}"
                log_error(msg)
                raise ValueError(msg)

            # Combine bricks using CadQuery's context solid behavior
            tile_workplane = tile_workplane.union(brick_model.translate((x_offset, 0, z_offset)))
            x_offset += brick_params["brick_length"] / (2 if j % 2 else 1)

        logging.debug(f"🔹 Row {i + 1} completed at z_offset {z_offset}")

    logging.debug("✅ DEBUG: Tile Assembly Completed!")
    return tile_workplane
