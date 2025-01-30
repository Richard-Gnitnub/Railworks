import cadquery as cq

def create_full_brick_aligned(config):
    """Creates a full-sized brick with chamfered edges to simulate mortar."""
    length, width, height, chamfer = (
        config["brick_length"], config["brick_width"], config["brick_height"], config["mortar_chamfer"]
    )
    
    brick = (
        cq.Workplane("XY")
        .box(length, width, height)
        .edges("|Z or |X ")  
        .chamfer(chamfer)  
    )
    return brick.translate((length / 2, width / 2, height / 2))

def create_half_brick_aligned(config):
    """Creates a half-sized brick with chamfered edges to simulate mortar."""
    length, width, height, chamfer = (
        config["brick_length"] / 2, config["brick_width"], config["brick_height"], config["mortar_chamfer"]
    )

    brick = (
        cq.Workplane("XY")
        .box(length, width, height)
        .edges("|Z or |X ")  
        .chamfer(chamfer)  
    )
    return brick.translate((length / 2, width / 2, height / 2))
