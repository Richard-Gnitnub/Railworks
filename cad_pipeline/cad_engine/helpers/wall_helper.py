import cadquery as cq
from cad_pipeline.cad_engine.helpers.assemble_brick_tile import assemble_brick_tile

def assemble_wall(parameters):
    """
    Assembles a full wall using stacked brick tiles.
    """
    wall_width = parameters["wall_width"]
    wall_height = parameters["wall_height"]
    tile_height = parameters["tile_height"]  
    tile_width = parameters["tile_width"]
    bond_pattern = parameters["bond_pattern"]

    wall_assembly = cq.Assembly()

    num_tiles_high = int(wall_height / tile_height)
    num_tiles_wide = int(wall_width / tile_width)

    for row in range(num_tiles_high):
        for col in range(num_tiles_wide):
            tile_config = {
                "tile_width": tile_width,
                "row_repetition": tile_height,
                "bond_pattern": bond_pattern,
                "brick_length": parameters["brick_length"],
                "brick_width": parameters["brick_width"],
                "brick_height": parameters["brick_height"],
                "mortar_chamfer": parameters["mortar_chamfer"]
            }

            tile = assemble_brick_tile(tile_config)
            wall_assembly.add(tile, loc=cq.Location(cq.Vector(col * tile_width, 0, row * tile_height)))

    return wall_assembly
