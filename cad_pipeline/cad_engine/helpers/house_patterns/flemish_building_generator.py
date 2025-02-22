import logging
import cadquery as cq
from ocp_vscode import show_object

# Global import/export utilities
from cad_pipeline.cad_engine.globals.import_handler import import_step_subassembly
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from cad_pipeline.models.assembly import Assembly

# Import our new helper modules
from cad_pipeline.cad_engine.helpers.building_corner import create_corner_from_walls
from cad_pipeline.cad_engine.helpers.replicate_corner import replicate_corner_by_mirror
from cad_pipeline.cad_engine.helpers.transform_wall import transform_wall  # if needed for additional transforms

# Import the global filename handler from the globals folder
from cad_pipeline.cad_engine.globals.filename_handler import generate_export_filename

# Import the wall generator to auto-regenerate if needed
from cad_pipeline.cad_engine.helpers.wall_patterns.flemish_wall_generator import generate_flemish_wall

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def generate_flemish_building():
    """
    Generates a building by:
      1. Retrieving the 'flemish_building_generator' Assembly from the DB.
      2. Retrieving dynamic parameters from the assembly:
         - 'front_offset' and 'left_offset' for aligning walls,
         - 'replication_translation' for positioning the mirrored corner,
         - and any other necessary parameters.
      3. Importing a cached wall solid from "flemish_wall_generator.step" (auto-regenerated if missing).
      4. Deriving a front wall (as-is) and a left wall (rotated -90°) from the imported wall.
      5. Creating a corner by combining these two walls (via create_corner_from_walls).
      6. Replicating the corner using mirroring (via replicate_corner_by_mirror) to form the opposite corner.
      7. Uniting both corners to form the complete building.
      8. Exporting and displaying the final building model.
    """
    logging.info("🚀 Starting Flemish Building Generation...")

    # 1. Retrieve the building assembly.
    building_assembly = retrieve_assembly("flemish_building_generator")
    if not building_assembly:
        logging.error("❌ Building assembly not found.")
        return None

    # 2. Retrieve dynamic parameters from the assembly.
    params = building_assembly.parameters
    try:
        front_offset = params["front_offset"]       # e.g. 1500
        left_offset  = params["left_offset"]        # e.g. 1000
        replication_translation = params["replication_translation"]  # e.g. [3000, 2000, 0]
        assemble_mode = params["assemble_mode"]
    except KeyError as e:
        logging.error(f"❌ Missing required parameter: {e}")
        return None

    # 3. Import the cached wall from "flemish_wall_generator.step".
    child_wall_assembly = retrieve_assembly("flemish_wall_generator")
    if not child_wall_assembly:
        logging.error("❌ Child wall assembly 'flemish_wall_generator' not found.")
        return None

    child_wall_file = generate_export_filename(child_wall_assembly.name, "step")
    logging.info(f"🔄 Importing wall solid from '{child_wall_file}'...")
    try:
        child_wall = import_step_subassembly(
            file_name=child_wall_file,
            generator_function=generate_flemish_wall  # Auto-regenerate if missing.
        )
        if child_wall is None:
            logging.error(f"❌ Failed to import wall solid from '{child_wall_file}'.")
            return None
    except Exception as e:
        logging.error(f"❌ Exception while importing wall solid: {e}")
        return None

    # 4. Derive front and left wall solids.
    # Front wall: Use the child wall as is.
    front_wall = child_wall
    # Left wall: Rotate the child wall -90° about Z.
    left_wall = transform_wall(child_wall, -90, (0, 0, 0))

    # 5. Create a corner from these two walls.
    # We apply translations so that the walls butt correctly:
    # For example, translate the front wall by (-front_offset, 0, 0) and left wall by (0, -left_offset, 0).
    corner = create_corner_from_walls(front_wall, left_wall,
                                      front_translation=(-front_offset, 0, 0),
                                      left_translation=(0, -left_offset, 0))
    logging.info("✅ Corner created successfully.")

    # 6. Replicate the corner using mirroring.
    opposite_corner = replicate_corner_by_mirror(corner, mirror_plane="YZ", translation=replication_translation)
    logging.info("✅ Opposite corner replicated successfully.")

    # 7. Combine the two corners into one building model.
    building_model = corner.union(opposite_corner)
    logging.info("✅ Building model assembled by uniting corners.")

    # 8. Export the building model.
    export_flemish_building(building_model, building_assembly)

    # 9. Display the building.
    logging.info("🎨 Displaying Flemish Building in Viewer...")
    show_object(building_model, name="Flemish Building")

    logging.info("✅ Flemish Building Generation Complete")
    return building_model

def retrieve_assembly(name: str):
    """
    Retrieves an assembly by name from the database.
    
    :param name: Assembly name.
    :return: Assembly object or None if not found.
    """
    try:
        return Assembly.objects.get(name=name)
    except Assembly.DoesNotExist:
        logging.error(f"❌ ERROR: Assembly '{name}' not found in the database.")
        return None

def export_flemish_building(building_model, building_assembly):
    """
    Exports the building model using the global export handler.
    
    :param building_model: The final CadQuery solid or assembly representing the building.
    :param building_assembly: The assembly object from the database.
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
    generate_flemish_building()
