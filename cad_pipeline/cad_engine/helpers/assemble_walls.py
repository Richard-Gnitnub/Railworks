import cadquery as cq

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
    if mode == "union":
        return front.union(back).union(left).union(right)
    else:
        building_assembly = cq.Assembly()
        building_assembly.add(front, name="front_wall")
        building_assembly.add(back, name="back_wall")
        building_assembly.add(left, name="left_wall")
        building_assembly.add(right, name="right_wall")
        return building_assembly
