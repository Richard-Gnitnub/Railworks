import cadquery as cq

def create_full_brick(config):
    """
    Creates a full brick with chamfered edges.
    :param config: Dictionary containing brick dimensions.
    :return: CadQuery solid representing a full brick.
    """
    brick = (
        cq.Workplane("XY")
        .box(config["brick_length"], config["brick_width"], config["brick_height"])
        .edges("|Z or |X")
        .chamfer(config["mortar_chamfer"])
    )
    return brick.translate((config["brick_length"] / 2, config["brick_width"] / 2, config["brick_height"] / 2))


def create_half_brick(config):
    """
    Creates a half brick with chamfered edges.
    :param config: Dictionary containing brick dimensions.
    :return: CadQuery solid representing a half brick.
    """
    brick = (
        cq.Workplane("XY")
        .box(config["brick_length"] / 2, config["brick_width"], config["brick_height"])
        .edges("|Z or |X")
        .chamfer(config["mortar_chamfer"])
    )
    return brick.translate((config["brick_length"] / 4, config["brick_width"] / 2, config["brick_height"] / 2))


def assemble_tile(config):
    """
    Assembles a tile based on the Flemish bond pattern.
    :param config: Dictionary containing tile configuration.
    :return: A CadQuery Assembly object representing the tile.
    """
    tile_assembly = cq.Assembly()

    row_repetition = config["row_repetition"]
    tile_width = config["tile_width"]
    offset_X = config.get("offset_X", 0)

    for i in range(row_repetition):
        row_assembly = cq.Assembly()
        half_brick = create_half_brick(config)
        full_brick = create_full_brick(config)

        # Alternate row shifting for Flemish bond
        row_x_offset = -config["brick_length"] / 2 if i % 2 != 0 else 0
        x_offset = row_x_offset

        for j in range(tile_width):
            if j % 2 == 0:
                row_assembly.add(
                    full_brick,
                    loc=cq.Location(cq.Vector(x_offset, 0, 0)),
                    name=f"Full Brick Row{i}-Col{j}"
                )
                x_offset += config["brick_length"]
            else:
                row_assembly.add(
                    half_brick,
                    loc=cq.Location(cq.Vector(x_offset, 0, 0)),
                    name=f"Half Brick Row{i}-Col{j}"
                )
                x_offset += config["brick_length"] / 2

        # Z Offset ensures stacking
        z_offset = i * config["brick_height"]
        tile_assembly.add(
            row_assembly,
            loc=cq.Location(cq.Vector(offset_X * i, 0, z_offset)),
            name=f"Row {i}"
        )

    return tile_assembly
