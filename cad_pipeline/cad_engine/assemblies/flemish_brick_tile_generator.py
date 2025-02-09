import cadquery as cq
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.helpers.assemble_brick_tile import assemble_brick_tile
from cad_pipeline.cad_engine.globals.export_handler import export_assembly
from cad_pipeline.cad_engine.globals.cache_manager import cache_model, retrieve_cached_model, is_cached
from ocp_vscode import show_object


def generate_flemish_brick_tile():
    """
    Generates a Flemish Brick Tile using parameters from the database, handles caching, and exports the result.
    """
    print("\n🚀 DEBUG: Starting Dynamic Flemish Brick Tile Assembly & Export Test...\n")

    # ✅ **Step 1: Retrieve Assembly and Brick Parameters from MPTT Tree**
    tile_assembly = Assembly.objects.get(name="generate_flemish_brick_tile")
    brick_geometry = Assembly.objects.get(name="brick_geometry")

    tile_parameters = tile_assembly.parameters  # Tile-specific parameters
    brick_parameters = brick_geometry.parameters  # Brick dimensions

    print(f"\n✅ Retrieved Tile Parameters: {tile_parameters}")
    print(f"✅ Retrieved Brick Parameters: {brick_parameters}")

    # ✅ **Step 2: Check Cache Before Regeneration**
    cache_key = f"brick_tile_{tile_assembly.id}"
    if is_cached(cache_key):
        print(f"\n✅ Retrieved Cached Model: {cache_key}")
        tile_model = retrieve_cached_model(cache_key)
    else:
        print("\n🔧 DEBUG: Generating New Tile Model...\n")
        tile_model = assemble_brick_tile(tile_assembly, [brick_parameters])
        cache_model(tile_model, cache_key, "step")

    # ✅ **Step 3: Export Tile Using `export_handler.py`**
    try:
        export_config = {
            "export_formats": ["step", "stl"],
            "file_name": f"{tile_assembly.name}_export",
            "component": tile_assembly  # ✅ Pass the component for database reference
        }
        exported_files = export_assembly(tile_model, **export_config)

        print("\n✅ Tile Export Completed!")
        for fmt, file_data in exported_files.items():
            print(f"   - Exported Format: {fmt.upper()}, Size: {len(file_data.file_data)} bytes")

    except Exception as e:
        raise RuntimeError(f"❌ Failed to export tile: {e}")

    # ✅ **Step 4: Visualize the Tile**
    print("\n🎨 Displaying Tile in Viewer...\n")
    show_object(tile_model, name="Brick Tile 1")

    print("\n✅ Test Complete!\n")
