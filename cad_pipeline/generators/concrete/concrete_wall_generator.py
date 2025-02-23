import logging
import cadquery as cq
from ocp_vscode import show_object
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from cad_pipeline.cad_engine.helpers.calculate_wall_dimensions import calculate_wall_dimensions
from cad_pipeline.cad_engine.helpers.cutouts import apply_cutouts
from cad_pipeline.generators.generator_strategy import IGenerator
from cad_pipeline.generators.concrete.concrete_brick_tile_generator import FlemishBrickTileGenerator
from cad_pipeline.cad_engine.globals.error_handler import log_error

class FlemishWallGenerator(IGenerator):
    def generate(self, wall_assembly: Assembly):
        """
        Generates a Flemish Brick Wall using the strategy pattern.
        """
        logging.info("🚀 Starting Flemish Wall Generation...")

        # Calculate wall dimensions.
        dimensions = calculate_wall_dimensions()
        if dimensions is None:
            log_error("❌ Failed to calculate wall dimensions")
            return None
        logging.info(f"Calculated dimensions: {dimensions}")

        # Generate the tile assembly required for the wall.
        tile_model = self.generate_tile_assembly(wall_assembly)
        if tile_model is None:
            log_error("❌ Failed to generate tile assembly")
            return None

        # Retrieve manual cutouts from wall parameters.
        manual_cutouts = wall_assembly.parameters.get("cutouts", [])
        wall_with_cutouts = self.apply_wall_cutouts(tile_model, manual_cutouts)
        if wall_with_cutouts is None:
            log_error("❌ Failed to apply cutouts to wall")
            return None

        # Export the newly generated wall.
        self.export_flemish_wall(wall_with_cutouts, wall_assembly)

        # Display the wall model.
        logging.info("🎨 Displaying Flemish Wall in Viewer...")
        show_object(wall_with_cutouts, name="Flemish Wall")
        logging.info("✅ Flemish Wall Generation Complete")
        return wall_with_cutouts

    def generate_tile_assembly(self, wall_assembly: Assembly) -> cq.Workplane:
        """
        Generates the tile assembly via the brick tile generator.
        """
        tile_assembly_name = "flemish_brick_tile_generator"
        try:
            from cad_pipeline.models import Assembly
            tile_assembly = Assembly.objects.get(name=tile_assembly_name)
        except Assembly.DoesNotExist:
            log_error(f"❌ Tile assembly '{tile_assembly_name}' not found in DB")
            return None

        generator = FlemishBrickTileGenerator()
        tile_model = generator.generate(tile_assembly)
        if tile_model is None:
            log_error("❌ ERROR: Failed to generate tile model")
            return None
        logging.info("✅ Successfully generated tile model.")
        return tile_model

    def apply_wall_cutouts(self, tile_model: cq.Workplane, cutouts: list) -> cq.Workplane:
        """
        Applies manual cutouts to the wall model.
        """
        try:
            logging.info("🛠 Applying manual cutouts to the wall...")
            return apply_cutouts(tile_model, cutouts)
        except Exception as e:
            log_error("❌ ERROR: Failed to apply cutouts", e)
            return None

    def export_flemish_wall(self, wall_model: cq.Workplane, wall_assembly: Assembly):
        """
        Exports the wall model using the global export handler.
        """
        try:
            export_config = {
                "export_formats": ["step", "stl"],
                "component": wall_assembly
            }
            exported_files = export_assembly(wall_model, **export_config)
            logging.info("✅ Wall Export Completed!")
            for fmt, exported_file in exported_files.items():
                logging.info(f"   - Exported Format: {fmt.upper()}, Size: {len(exported_file.file_data)} bytes")
        except Exception as e:
            log_error("❌ ERROR: Failed to export wall", e)
