import cadquery as cq
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.helpers.assemble_brick_tile import assemble_brick_tile
from ocp_vscode import show_object

# Test Script for Assembling a Brick Tile
def test_assemble_brick_tile():
    try:
        # Step 1: Create or Retrieve the Tile Assembly
        tile, _ = Assembly.objects.get_or_create(
            name="Brick Tile 1",
            type="tile",
            defaults={
                "parameters": {
                    "tile_width": 4,
                    "row_repetition": 2,
                    "bond_pattern": "flemish",
                    "brick_length": 215,
                    "brick_width": 102.5,
                    "brick_height": 65,
                    "mortar_chamfer": 10,
                }
            }
        )
        print(f"\n Tile Created/Retrieved: {tile.name}")
    except Exception as e:
        print(f" Failed to create or retrieve tile: {e}")
        raise

    try:
        # Step 2: Retrieve Bricks
        children = Assembly.objects.filter(parent=tile)
        brick_parameters_list = [brick.parameters for brick in children]
        print(f"\n Tile '{tile.name}' has {len(brick_parameters_list)} bricks.")
        print(f" Brick Parameters Retrieved: {brick_parameters_list}")
    except Exception as e:
        print(f" Failed to retrieve child bricks: {e}")
        raise

    try:
        # Step 3: Generate the Tile Assembly
        print("\n DEBUG: Generating Tile Assembly...\n")
        tile_model = assemble_brick_tile(tile, brick_parameters_list)
        print(f" Tile Model Assembled: {tile_model}")

        # Step 3a: Export the Tile for External Validation
        cq.exporters.export(tile_model, "tile_assembly.step")
        print(" Tile assembly exported as 'tile_assembly.step'.")
    except Exception as e:
        print(f" Failed to assemble tile: {e}")
        raise

    try:
        # Step 4: Visualize the Tile in the Viewer
        if "tile_model" in locals():
            print("\n DEBUG: Showing Tile in Viewer...\n")
            show_object(tile_model, name="Brick Tile 1")
        else:
            print(" Tile model is undefined, cannot visualize.")
    except Exception as e:
        print(f" Failed to visualize tile: {e}")

# Execute the test
if __name__ == "__main__":
    test_assemble_brick_tile()
