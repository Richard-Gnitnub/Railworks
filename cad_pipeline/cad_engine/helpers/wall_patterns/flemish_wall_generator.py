import cadquery as cq
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.helpers.tile_patterns.flemish_brick_tile_generator import generate_flemish_brick_tile
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from ocp_vscode import show_object

def generate_flemish_wall():
    """
    Generates a Flemish brick wall by placing completed Flemish tiles into a grid.
    The tile structure and pattern are pre-defined and retrieved from the database.
    """
    print("\n🚀 DEBUG: Starting Flemish Brick Wall Assembly...\n")

    # ✅ **Step 1: Retrieve Wall Parameters**
    wall_assembly = Assembly.objects.get(name="flemish_wall")
    wall_parameters = wall_assembly.parameters
    wall_width = wall_parameters["wall_width"]  # Number of tiles wide
    wall_height = wall_parameters["wall_height"]  # Number of tiles tall

    print(f"✅ Wall Parameters: Width={wall_width} tiles, Height={wall_height} tiles")

    # ✅ **Step 2: Arrange Tiles in a Grid**
    wall_model = cq.Workplane("XY")

    for row in range(wall_height):
        for col in range(wall_width):
            tile_instance = generate_flemish_brick_tile()  # Generate a fresh tile each time

            # ✅ Compute X, Z positions dynamically (each tile occupies one cell)
            x_offset = col
            z_offset = row

            print(f"🔹 Placing tile at Row {row+1}, Column {col+1} at (X={x_offset}, Z={z_offset})")

            # ✅ Translate tile and add to the wall model
            translated_tile = tile_instance.translate((x_offset, 0, z_offset))
            wall_model = wall_model.union(translated_tile)

    print("\n✅ Wall Assembly Completed!")

    # ✅ **Step 3: Export Wall**
    try:
        export_config = {
            "export_formats": ["step", "stl"],
            "file_name": "flemish_wall_export",
            "component": wall_assembly
        }
        exported_files = export_assembly(wall_model, **export_config)

        print("\n✅ Wall Export Completed!")
        for fmt, file_data in exported_files.items():
            print(f"   - Exported Format: {fmt.upper()}, Size: {len(file_data.file_data)} bytes")

    except Exception as e:
        raise RuntimeError(f"❌ Failed to export wall: {e}")

    # ✅ **Step 4: Visualize Wall**
    print("\n🎨 Displaying Flemish Wall in Viewer...\n")
    show_object(wall_model, name="Flemish Wall")

    print("\n✅ Test Complete!\n")
