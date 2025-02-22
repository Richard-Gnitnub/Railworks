import logging
import cadquery as cq
from datetime import datetime
from ocp_vscode import show_object

from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.globals.import_handler import import_step_subassembly
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from cad_pipeline.cad_engine.globals.filename_handler import generate_export_filename
from cad_pipeline.cad_engine.globals.metadata_handler import update_last_export
from cad_pipeline.cad_engine.helpers.calculate_wall_dimensions import calculate_wall_dimensions
from cad_pipeline.cad_engine.helpers.cutouts import apply_cutouts

from cad_pipeline.generators.generator_strategy import IGenerator
from cad_pipeline.generators.concrete.concrete_brick_tile_generator import FlemishBrickTileGenerator

class FlemishWallGenerator(IGenerator):
    def generate(self, wall_assembly: Assembly):
        """
        Generates a Flemish Brick Wall using the strategy pattern.
        """
        logging.info("🚀 Starting Flemish Brick Wall Generation...")

        # 1. Calculate wall dimensions.
        dimensions = calculate_wall_dimensions()
        if dimensions is None:
            logging.error("❌ Failed to calculate wall dimensions.")
            return None
        logging.info(f"Calculated dimensions: {dimensions}")

        # 2. Import or regenerate the tile assembly.
        tile_model = self.import_tile_assembly(wall_assembly)
        if tile_model is None:
            logging.error("❌ Failed to import tile assembly.")
            return None

        # 3. Retrieve manual cutouts from the wall assembly parameters.
        manual_cutouts = wall_assembly.parameters.get("cutouts", [])
        if not manual_cutouts:
            logging.warning("⚠️ No manual cutouts defined; proceeding without cutouts.")

        wall_with_cutouts = self.apply_wall_cutouts(tile_model, manual_cutouts)
        if wall_with_cutouts is None:
            logging.error("❌ Failed to apply cutouts to wall.")
            return None

        # 4. Export the final wall model.
        self.export_flemish_wall(wall_with_cutouts, wall_assembly)

        # 5. Display the wall in the 3D viewer.
        logging.info("🎨 Displaying Flemish Wall in Viewer...")
        show_object(wall_with_cutouts, name="Flemish Wall")
        logging.info("✅ Flemish Brick Wall Generation Complete")
        return wall_with_cutouts

    def import_tile_assembly(self, wall_assembly: Assembly) -> cq.Workplane:
        """
        Imports or regenerates the tile assembly via the new brick tile strategy.
        """
        tile_assembly_name = "flemish_brick_tile_generator"
        try:
            from cad_pipeline.models import Assembly
            tile_assembly = Assembly.objects.get(name=tile_assembly_name)
        except Assembly.DoesNotExist:
            logging.error(f"❌ Tile assembly '{tile_assembly_name}' not found in DB.")
            return None

        tile_file_name = generate_export_filename(
            f"{wall_assembly.name}_{tile_assembly_name}", 
            "step",
            user_defined_name=tile_assembly.parameters.get("export_filename")
        )

        logging.info(f"🔄 Attempting to import '{tile_file_name}' from cache...")

        # Adapter function that calls the strategy for brick tile generation.
        def tile_generator_func():
            generator = FlemishBrickTileGenerator()
            return generator.generate(tile_assembly)

        try:
            tile_model = import_step_subassembly(tile_file_name, generator_function=tile_generator_func)
            if tile_model is None:
                logging.error(f"❌ ERROR: Failed to import or generate '{tile_file_name}'.")
                return None
            logging.info(f"✅ Successfully imported or regenerated '{tile_file_name}'.")
            return tile_model
        except Exception as e:
            logging.error(f"❌ ERROR: Tile import/generation failed: {e}")
            return None

    def apply_wall_cutouts(self, tile_model: cq.Workplane, cutouts: list) -> cq.Workplane:
        """
        Applies manual cutouts to the wall model.
        """
        try:
            logging.info("🛠 Applying manual cutouts to the wall...")
            return apply_cutouts(tile_model, cutouts)
        except Exception as e:
            logging.error(f"❌ ERROR: Failed to apply cutouts: {e}")
            return None

    def export_flemish_wall(self, wall_model: cq.Workplane, wall_assembly: Assembly):
        """
        Exports the wall model and updates export metadata.
        """
        try:
            export_config = {
                "export_formats": ["step", "stl"],
                "component": wall_assembly
            }
            exported_files = export_assembly(wall_model, **export_config)
            logging.info("✅ Wall Export Completed!")
            for fmt, file_data in exported_files.items():
                logging.info(f"   - Exported Format: {fmt.upper()}, Size: {len(file_data.file_data)} bytes")
            update_last_export(wall_assembly.name, datetime.now().isoformat())
        except Exception as e:
            logging.error(f"❌ ERROR: Failed to export wall: {e}")

if __name__ == "__main__":
    # For testing within the Django shell.
    # from cad_pipeline.models import Assembly
    # wall_assembly = Assembly.objects.get(name="flemish_wall_generator")
    # wall_model = FlemishWallGenerator().generate(wall_assembly)
    pass
