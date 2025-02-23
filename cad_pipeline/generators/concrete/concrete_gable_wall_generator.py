import logging
import cadquery as cq
from ocp_vscode import show_object
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.globals.error_handler import log_error
from cad_pipeline.generators.generator_strategy import IGenerator
from cad_pipeline.generators.concrete.concrete_brick_tile_generator import FlemishBrickTileGenerator
# Import the new pitched cut functions from cutouts.py
from cad_pipeline.cad_engine.helpers.cutouts import apply_pitched_cut

class FlemishGableWallGenerator(IGenerator):
    """
    Concrete generator for creating a Flemish Gable Wall with a pitched top cut.
    """
    def generate(self, gable_assembly: Assembly):
        logging.info("🚀 Starting Flemish Gable Wall Generation...")

        # Retrieve the assembly if not passed in
        if not gable_assembly:
            gable_assembly = self.retrieve_assembly("flemish_gable_wall_generator")
            if not gable_assembly:
                log_error("❌ Gable wall assembly not found.")
                return None

        # Extract required parameters from the assembly.
        params = gable_assembly.parameters
        try:
            total_width  = params["width"]          # Total width of the wall.
            eave_height  = params["eave_height"]      # Height of the wall at the eave.
            apex_height  = params["apex_height"]      # Height at the apex relative to the eave.
            thickness    = params.get("thickness", 10)  # Wall thickness; default is 10 mm.
        except KeyError as e:
            log_error(f"❌ Missing required parameter in gable assembly: {e}")
            return None

        # Create a base rectangular wall: a simple extruded profile.
        try:
            base_wall_profile = cq.Workplane("XY").rect(total_width, eave_height).extrude(thickness)
            logging.info("✅ Base wall created.")
        except Exception as e:
            log_error(f"❌ Failed to create base wall: {e}")
            return None

        # Apply the pitched cut to form the gable top.
        try:
            pitch_params = {
                "width": total_width,
                "eave_height": eave_height,
                "apex_height": apex_height,
                "thickness": thickness,
                "x_offset": 0,  # Adjust if needed
                "z_offset": 0,  # Adjust if needed
            }
            # This function will subtract a wedge from the base wall to form the pitched top.
            gable_wall = apply_pitched_cut(base_wall_profile, pitch_params)
            logging.info("✅ Pitched cut applied to create gable wall.")
        except Exception as e:
            log_error(f"❌ Error applying pitched cut: {e}")
            return None

        # Optionally, merge a tile assembly for the gable wall (if required).
        tile_model = self.generate_tile_assembly()
        if tile_model:
            gable_wall = gable_wall.union(tile_model)
            logging.info("✅ Tile assembly merged with gable wall.")

        # Export and display the gable wall.
        try:
            self.export_gable_wall(gable_wall, gable_assembly)
        except Exception as e:
            log_error(f"❌ Error exporting gable wall: {e}")
        logging.info("🎨 Displaying Gable Wall in Viewer...")
        show_object(gable_wall, name="Flemish Gable Wall")
        logging.info("✅ Flemish Gable Wall Generation Complete")
        return gable_wall

    def retrieve_assembly(self, name: str):
        """
        Retrieves an assembly by name from the database.
        """
        try:
            from cad_pipeline.models.assembly import Assembly
            return Assembly.objects.get(name=name)
        except Assembly.DoesNotExist:
            logging.error(f"❌ ERROR: Assembly '{name}' not found in the database.")
            return None

    def export_gable_wall(self, wall_model: cq.Workplane, assembly: Assembly):
        """
        Exports the gable wall model using the global export handler.
        """
        try:
            from cad_pipeline.cad_engine.globals.export_handler import export_assembly
            export_config = {
                "export_formats": ["step", "stl"],
                "component": assembly
            }
            exported_files = export_assembly(wall_model, **export_config)
            logging.info("✅ Gable Wall Export Completed!")
            for fmt, file_data in exported_files.items():
                logging.info(f"   - Exported Format: {fmt.upper()}, Size: {len(file_data.file_data)} bytes")
        except Exception as e:
            log_error(f"❌ ERROR: Failed to export gable wall: {e}", e)

    def generate_tile_assembly(self):
        """
        Generates a tile assembly for the gable wall.
        You can use the existing brick tile generator or provide custom logic.
        For now, we return a dummy tile model.
        """
        try:
            tile_generator = FlemishBrickTileGenerator()
            # For demonstration, return a simple box as a dummy tile.
            return cq.Workplane("XY").box(10, 10, 2)
        except Exception as e:
            log_error(f"❌ Error generating tile assembly for gable wall: {e}", e)
            return None
