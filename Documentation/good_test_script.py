import cadquery as cq
import io
import tempfile
from django.core.cache import cache
from django.db import IntegrityError
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.models.exported_file import ExportedFile
from cad_pipeline.cad_engine.helpers.assemble_brick_tile import assemble_brick_tile
from cad_pipeline.cad_engine.export_handler import export_assembly_cached
from ocp_vscode import show_object

print("\n🚀 DEBUG: Starting Brick Tile Assembly & Export Test...\n")

# ✅ **Step 1: Retrieve or Create Tile Assembly**
tile = None

try:
    tile = Assembly.objects.get(name__iexact="Brick Tile 1", type="brick_tile")
    print(f"\n✅ Retrieved Existing Tile: {tile.name} (ID: {tile.id})")
except Assembly.DoesNotExist:
    try:
        tile = Assembly.objects.create(
            name="Brick Tile 1",
            type="brick_tile",
            parameters={
                "tile_width": 4,
                "row_repetition": 2,
                "bond_pattern": "flemish",
                "brick_length": 215,
                "brick_width": 102.5,
                "brick_height": 65,
                "mortar_chamfer": 10,
            },
        )
        print(f"\n✅ Created New Tile: {tile.name} (ID: {tile.id})")
    except IntegrityError:
        tile = Assembly.objects.filter(name__iexact="Brick Tile 1", type="brick_tile").first()
        print(f"\n⚠️ Warning: Tile already exists. Using existing tile (ID: {tile.id}).")

if not tile:
    raise RuntimeError("❌ Critical Error: Tile could not be retrieved or created.")

# ✅ **Step 2: Retrieve or Create Bricks**
brick_definitions = [
    {"name": "Full Brick", "length": 215},
    {"name": "Half Brick", "length": 107.5},
]

bricks = []
for brick_def in brick_definitions:
    brick, _ = Assembly.objects.get_or_create(
        name=brick_def["name"],
        type="brick",
        parent=tile,
        defaults={
            "parameters": {
                "brick_length": brick_def["length"],
                "brick_width": 102.5,
                "brick_height": 65,
                "mortar_chamfer": 10,
            }
        },
    )
    bricks.append(brick)

print(f"✅ Bricks Created/Retrieved: {[brick.name for brick in bricks]}")

# ✅ **Step 3: Retrieve Parameters of Bricks**
brick_parameters_list = [brick.parameters for brick in bricks]
print(f"\n✅ Tile '{tile.name}' has {len(brick_parameters_list)} bricks.")
print(f"✅ Brick Parameters Retrieved: {brick_parameters_list}")

# ✅ **Step 4: Generate or Retrieve Tile Assembly**
cache_key = f"exported_tile_{tile.id}"
cached_step_data = cache.get(cache_key)

if cached_step_data:
    try:
        # ✅ Load the STEP file back into CadQuery
        with tempfile.NamedTemporaryFile(delete=False, suffix=".step") as tmp_step:
            tmp_step.write(cached_step_data)
            tmp_step_path = tmp_step.name
        tile_model = cq.importers.importStep(tmp_step_path)
        print("\n✅ Retrieved Tile Model from Cache!")
    except Exception:
        print("\n⚠️ Warning: Cache deserialization failed. Recomputing...")
        tile_model = None
else:
    tile_model = None

# **Regenerate if not found in cache**
if not tile_model:
    try:
        print("\n🔧 DEBUG: Generating Tile Assembly...\n")
        tile_model = assemble_brick_tile(tile, brick_parameters_list)

        # ✅ **Convert to STEP format and cache**
        with tempfile.NamedTemporaryFile(delete=False, suffix=".step") as tmp_step:
            tmp_step_path = tmp_step.name
        cq.exporters.export(tile_model, tmp_step_path)

        with open(tmp_step_path, "rb") as step_file:
            step_data = step_file.read()
            cache.set(cache_key, step_data, timeout=86400)

        print("✅ Tile Assembly Serialized and Cached as STEP.")

    except Exception as e:
        raise RuntimeError(f"❌ Failed to assemble tile: {e}")

# ✅ **Step 5: Export the Tile**
if tile_model:
    try:
        export_config = {"export_formats": ["step", "stl"], "file_name": f"{tile.name}_export"}
        exported_files = export_assembly_cached(tile_model, export_config)

        print("\n✅ Tile Export Completed!")
        for fmt, file_data in exported_files.items():
            print(f"   - Exported Format: {fmt.upper()}, Size: {len(file_data)} bytes")

            # ✅ **Store the exported file in the database**
            ExportedFile.store_exported_file(tile, fmt, file_data)

    except Exception as e:
        raise RuntimeError(f"❌ Failed to export tile: {e}")

# ✅ **Step 6: Visualize the Tile in the Viewer**
if tile_model:
    print("\n🎨 DEBUG: Showing Tile in Viewer...\n")
    show_object(tile_model, name="Brick Tile 1")
else:
    print("❌ Tile model is undefined, cannot visualize.")

print("\n✅ Test Complete!\n")
