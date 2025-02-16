import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def regular_grid(width, height, spacing_x, spacing_y, offset_x=0, offset_y=0):
    """
    Generates a grid of cutout positions based on the provided dimensions.
    
    :param width: Total width of the wall.
    :param height: Total height of the wall.
    :param spacing_x: Horizontal spacing between cutouts.
    :param spacing_y: Vertical spacing between cutouts.
    :param offset_x: Horizontal offset.
    :param offset_y: Vertical offset.
    :return: List of dictionaries with grid coordinates and default cutout dimensions.
    """
    grid = []
    x = offset_x
    while x < width:
        z = offset_y
        while z < height:
            grid.append({
                "x": x,
                "z": z,
                "width": 10,   # default cutout width; adjust as needed
                "height": 10,  # default cutout height; adjust as needed
                "depth": 5     # default cutout depth; adjust as needed
            })
            z += spacing_y
        x += spacing_x
    logging.info(f"✅ Generated grid with {len(grid)} cutout positions.")
    return grid
