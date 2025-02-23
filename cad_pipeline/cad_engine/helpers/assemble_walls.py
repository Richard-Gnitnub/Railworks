import cadquery as cq
import logging
from cad_pipeline.cad_engine.globals.error_handler import log_error

def assemble_walls(front, back, left, right, mode="union"):
    """
    Assembles four walls into a building model.

    :param front: Front wall solid.
    :param back: Back wall solid.
    :param left: Left wall solid.
    :param right: Right wall solid.
    :param mode: "union" to combine into one solid, or "assembly" to keep parts separate.
    :return: The final building model.
    """
    logging.debug(f"Assembling walls with mode: {mode}")
    try:
        if mode == "union":
            building_model = front.union(back).union(left).union(right)
            logging.debug("Walls assembled using union.")
            return building_model
        else:
            building_assembly = cq.Assembly()
            building_assembly.add(front, name="front_wall")
            building_assembly.add(back, name="back_wall")
            building_assembly.add(left, name="left_wall")
            building_assembly.add(right, name="right_wall")
            logging.debug("Walls assembled into an assembly.")
            return building_assembly
    except Exception as e:
        log_error("Error in assemble_walls", e)
        raise
