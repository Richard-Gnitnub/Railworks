import logging
import cadquery as cq
from ocp_vscode import show_object

from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.globals.import_handler import import_step_subassembly
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from cad_pipeline.cad_engine.globals.filename_handler import generate_export_filename

from cad_pipeline.cad_engine.helpers.building_corner import create_corner_from_walls
from cad_pipeline.cad_engine.helpers.replicate_corner import replicate_corner_by_mirror
from cad_pipeline.cad_engine.helpers.transform_wall import transform_wall

from cad_pipeline.generators.generator_strategy import IGenerator
from cad_pipeline.generators.concrete.concrete_wall_generator import FlemishWallGenerator

class FlemishBuildingGenerator(IGenerator):
    def generate(self, building_assembly: Assembly):
        """
        Generates a Flemish Building using the strategy pattern.
        """
        logging.info("🚀 Starting Flemish Building Generation...")

        # 1. Retrieve the building assembly.
        building_assembly = self.retrieve_assembly("flemish_building_generator")
        if not building_assembly:
            logging.error("❌ Building assembly not found.")
            return None

        # 2. Retrieve dynamic parameters.
        params = building_assembly.parameters
        try:
            front_offset = params["front_offset"]
            left_offset  = params["left_offset"]
            replication_translation = params["replication_translation"]
            assemble_mode = params["assemble_mode"]
        except KeyError as e:
            logging.error(f"❌ Missing required parameter: {e}")
            return None

        # 3. Retrieve the wall assembly.
        child_wall_assembly = self.retrieve_assembly("flemish_wall_generator")
        if not child_wall_assembly:
            logging.error("❌ Child wall assembly 'flemish_wall_generator' not found.")
            return None

        # Use the updated filename handler with a possible user-defined filename.
        child_wall_file = generate_export_filename(
            child_wall_assembly.name,
            "step",
            user_defined_name=child_wall_assembly.parameters.get("export_filename")
        )
        logging.info(f"🔄 Importing wall solid from '{child_wall_file}'...")

        try:
            # Use the wall generator strategy to generate the wall.
            wall_generator = FlemishWallGenerator()
            child_wall = import_step_subassembly(
                child_wall_file,
                generator_function=lambda: wall_generator.generate(child_wall_assembly)
            )
            if child_wall is None:
                logging.error(f"❌ Failed to import wall solid from '{child_wall_file}'.")
                return None
        except Exception as e:
            logging.error(f"❌ Exception while importing wall solid: {e}")
            return None

        # 4. Derive front and left wall solids.
        front_wall = child_wall
        left_wall = transform_wall(child_wall, -90, (0, 0, 0))

        # 5. Create a corner from the walls.
        corner = create_corner_from_walls(front_wall, left_wall,
                                          front_translation=(-front_offset, 0, 0),
                                          left_translation=(0, -left_offset, 0))
        logging.info("✅ Corner created successfully.")

        # 6. Replicate the corner to form the opposite corner.
        opposite_corner = replicate_corner_by_mirror(corner, mirror_plane="YZ", translation=replication_translation)
        logging.info("✅ Opposite corner replicated successfully.")

        # 7. Unite both corners to assemble the building.
        building_model = corner.union(opposite_corner)
        logging.info("✅ Building model assembled by uniting corners.")

        # 8. Export and display the building.
        self.export_flemish_building(building_model, building_assembly)
        logging.info("🎨 Displaying Flemish Building in Viewer...")
        show_object(building_model, name="Flemish Building")
        logging.info("✅ Flemish Building Generation Complete")
        return building_model

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

    def export_flemish_building(self, building_model: cq.Workplane, building_assembly: Assembly):
        """
        Exports the building model using the global export handler.
        """
        try:
            export_config = {
                "export_formats": ["step", "stl"],
                "component": building_assembly
            }
            exported_files = export_assembly(building_model, **export_config)
            logging.info("✅ Building Export Completed!")
            for fmt, file_data in exported_files.items():
                logging.info(f"   - Exported Format: {fmt.upper()}, Size: {len(file_data.file_data)} bytes")
        except Exception as e:
            logging.error(f"❌ ERROR: Failed to export building: {e}")

if __name__ == "__main__":
    # For testing within the Django shell:
    # from cad_pipeline.models import Assembly
    # building_assembly = Assembly.objects.get(name="flemish_building_generator")
    # building_model = FlemishBuildingGenerator().generate(building_assembly)
    pass
