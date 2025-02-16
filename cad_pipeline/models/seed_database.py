import os
import django

# ✅ Ensure Django settings are loaded before imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railworks_project.settings")
django.setup()  # ✅ Initialize Django

# ✅ Import models AFTER Django setup
from cad_pipeline.models.nmra_standard import NMRAStandard
from cad_pipeline.models.assembly import Assembly

def seed_nmra_standards():
    """Populates the NMRAStandard model with predefined gauge data."""
    nmra_data = [
        {
            "name": "HO Scale",
            "scale_ratio": 87.1,
            "gauge_mm": 16.5,
            "clearance_mm": {"min_height": 50, "min_width": 30},
            "rail_profile": "Code 75 Bullhead"
        },
        {
            "name": "O Scale",
            "scale_ratio": 48.0,
            "gauge_mm": 32.0,
            "clearance_mm": {"min_height": 70, "min_width": 50},
            "rail_profile": "Code 100 Flat Bottom"
        },
        {
            "name": "N Scale",
            "scale_ratio": 160.0,
            "gauge_mm": 9.0,
            "clearance_mm": {"min_height": 40, "min_width": 25},
            "rail_profile": "Code 55 Flat Bottom"
        },
    ]

    for nmra in nmra_data:
        obj, created = NMRAStandard.objects.get_or_create(
            name=nmra["name"], defaults=nmra
        )
        if created:
            print(f"✅ Added NMRA Standard: {nmra['name']}")
        else:
            print(f"🔄 NMRA Standard {nmra['name']} already exists. Skipping...")

def seed_wall_assembly():
    """Populates the Assembly model with Wall Generator parameters."""
    wall_data = {
        "name": "generate_flemish_wall",
        "parameters": {
            "cutout_positions": [
                {"x": 200, "z": 150, "width": 50, "height": 100},
                {"x": 600, "z": 150, "width": 50, "height": 100},
                {"x": 400, "z": 350, "width": 100, "height": 200}
            ],
            "apply_boundary_logic": False  # Placeholder for future boundary logic
        }
    }

    obj, created = Assembly.objects.get_or_create(
        name=wall_data["name"], defaults={"parameters": wall_data["parameters"]}
    )
    
    if created:
        print(f"✅ Added Assembly: {wall_data['name']}")
    else:
        print(f"🔄 Assembly {wall_data['name']} already exists. Updating parameters...")
        obj.parameters = wall_data["parameters"]
        obj.save()
        print(f"✅ Updated {wall_data['name']} parameters!")

def seed_tile_assembly():
    """Populates the Assembly model with Tile Generator parameters."""
    tile_data = {
        "name": "generate_flemish_brick_tile",
        "parameters": {
            "tile_width": 4,
            "row_repetition": 2,
            "bond_pattern": "flemish"
        }
    }

    obj, created = Assembly.objects.get_or_create(
        name=tile_data["name"], defaults={"parameters": tile_data["parameters"]}
    )

    if created:
        print(f"✅ Added Assembly: {tile_data['name']}")
    else:
        print(f"🔄 Assembly {tile_data['name']} already exists. Updating parameters...")
        obj.parameters = tile_data["parameters"]
        obj.save()
        print(f"✅ Updated {tile_data['name']} parameters!")

def seed_brick_geometry():
    """Populates the Assembly model with Brick Geometry parameters."""
    brick_data = {
        "name": "brick_geometry",
        "parameters": {
            "brick_length": 215,
            "brick_width": 102.5,
            "brick_height": 65,
            "mortar_chamfer": 10
        }
    }

    obj, created = Assembly.objects.get_or_create(
        name=brick_data["name"], defaults={"parameters": brick_data["parameters"]}
    )

    if created:
        print(f"✅ Added Assembly: {brick_data['name']}")
    else:
        print(f"🔄 Assembly {brick_data['name']} already exists. Updating parameters...")
        obj.parameters = brick_data["parameters"]
        obj.save()
        print(f"✅ Updated {brick_data['name']} parameters!")

if __name__ == "__main__":
    print("🚀 Seeding NMRA Standards and Assemblies into the database...")
    seed_nmra_standards()
    seed_wall_assembly()
    seed_tile_assembly()
    seed_brick_geometry()
    print("✅ Database seeding complete!")
