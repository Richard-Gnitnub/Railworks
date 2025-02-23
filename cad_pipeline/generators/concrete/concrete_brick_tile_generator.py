import logging
import cadquery as cq
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.helpers.assemble_brick_tile import assemble_brick_tile
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from ocp_vscode import show_object
from cad_pipeline.generators.generator_strategy import IGenerator
from cad_pipeline.cad_engine.globals.error_handler import log_error

class FlemishBrickTileGenerator(IGenerator):
    def generate(self, assembly: Assembly):
        """
        Generates a Flemish Brick Tile using the parameters provided in the given assembly.
        
        The assembly should be the one corresponding to the tile generator (e.g. with name 
        "flemish_brick_tile_generator") and contain all required tile parameters.
        
        :param assembly: The Assembly object for the brick tile generator.
        :return: A CadQuery Workplane representing the assembled tile, or None on failure.
        """
        logging.info("Starting Flemish Brick Tile Assembly & Export...")
        
        try:
            # Retrieve tile parameters from the current assembly.
            tile_params = assembly.parameters
            # Retrieve or create the brick geometry assembly.
            brick_geometry, _ = Assembly.objects.get_or_create(name="brick_geometry")
            brick_params = brick_geometry.parameters
            logging.info("Retrieved brick geometry assembly.")
        except Exception as e:
            log_error("ERROR: Database lookup failed", e)
            return None

        # Validate required parameters.
        required_tile_params = ["tile_width", "row_repetition", "bond_pattern", "alignment_factor"]
        required_brick_params = ["brick_length", "brick_width", "brick_height", "mortar_chamfer"]

        missing_tile_keys = [k for k in required_tile_params if k not in tile_params]
        missing_brick_keys = [k for k in required_brick_params if k not in brick_params]

        if missing_tile_keys or missing_brick_keys:
            log_error(f"ERROR: Missing required parameters: {missing_tile_keys + missing_brick_keys}")
            return None

        logging.info(f"Tile Parameters: {tile_params}")
        logging.info(f"Brick Parameters: {brick_params}")

        # Assemble the tile using the provided parameters.
        try:
            tile_model = assemble_brick_tile(assembly, [brick_params])
            if tile_model is None:
                log_error("ERROR: assemble_brick_tile() returned None! Check input parameters")
                return None
            logging.info("Tile Assembly Completed.")
        except Exception as e:
            log_error("ERROR: Failed to assemble brick tile", e)
            return None

        # Export the assembled tile using the global export handler.
        try:
            export_assembly(tile_model, component=assembly)
            logging.info("Tile Export Completed!")
        except Exception as e:
            log_error("ERROR: Failed to export tile", e)
            return None

        # Visualise the tile in the 3D viewer.
        logging.info("Visualising Tile Model in Viewer...")
        show_object(tile_model, name="Flemish Brick Tile")
        logging.info("Flemish Brick Tile Generation Complete")
        return tile_model
