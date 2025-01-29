"""
Module: track_geometry.py
Description: Handles the generation of plain track tiles.
"""

import cadquery as cq
from resources.helpers.brick_helpers import create_track_section

def assemble_plain_track_tile(config: dict) -> cq.Assembly:
    """
    Assembles a plain track tile based on configuration.
    :param config: Dictionary containing track parameters.
    :return: CadQuery Assembly object representing the track tile.
    """
    track_assembly = cq.Assembly()
    track_length = config["track_length"]
    track_width = config["track_width"]
    track_height = config["track_height"]
    spacing = config["spacing"]

    # Create a basic track section
    track_section = create_track_section(config)

    # Define how many sections to generate
    num_sections = int(track_length / spacing)

    for i in range(num_sections):
        x_offset = i * spacing
        track_assembly.add(track_section, loc=cq.Location(cq.Vector(x_offset, 0, 0)), name=f"Track Section {i}")

    return track_assembly
