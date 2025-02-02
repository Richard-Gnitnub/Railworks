import django
import os

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railworks_project.settings")  # Update to match your project
django.setup()

from cad_pipeline.models import NMRAStandard, Parameter, Assembly

def seed_nmra_standards():
    """Populates NMRAStandard model with predefined gauge data."""
    nmra_data = [
        {"name": "HO Scale", "scale_ratio": 87.1, "gauge_mm": 16.5, "clearance_mm": {"min_height": 50, "min_width": 30}, "rail_profile": "Code 75 Bullhead"},
        {"name": "O Scale", "scale_ratio": 48.0, "gauge_mm": 32.0, "clearance_mm": {"min_height": 70, "min_width": 50}, "rail_profile": "Code 100 Flat Bottom"},
        {"name": "N Scale", "scale_ratio": 160.0, "gauge_mm": 9.0, "clearance_mm": {"min_height": 40, "min_width": 25}, "rail_profile": "Code 55 Flat Bottom"},
    ]

    for nmra in nmra_data:
        obj, created = NMRAStandard.objects.get_or_create(name=nmra["name"], defaults=nmra)
        if created:
            print(f"✅ Added NMRA Standard: {nmra['name']}")
        else:
            print(f"🔄 NMRA Standard {nmra['name']} already exists. Skipping...")

def seed_parameters():
    """Populates Parameter model with configurable values."""
    parameters = [
        {"name": "flemish", "value": "Flemish Bond", "parameter_type": "bond_pattern"},
        {"name": "stretcher", "value": "Stretcher Bond", "parameter_type": "bond_pattern"},
        {"name": "stack", "value": "Stack Bond", "parameter_type": "bond_pattern"},
        {"name": "step", "value": "STEP File", "parameter_type": "export_format"},
        {"name": "stl", "value": "STL File", "parameter_type": "export_format"},
        {"name": "max_tile_width", "value": {"value": 10}, "parameter_type": "tile_constraint"},
        {"name": "min_brick_size", "value": {"length": 200, "width": 100, "height": 50}, "parameter_type": "tile_constraint"},
    ]

    for param in parameters:
        obj, created = Parameter.objects.get_or_create(name=param["name"], defaults=param)
        if created:
            print(f"✅ Added Parameter: {param['name']}")
        else:
            print(f"🔄 Parameter {param['name']} already exists. Skipping...")

def seed_tile_generator_settings():
    """Populates Assembly model with tile generator settings."""
    tile_metadata = {
        "brick_length": 250,
        "brick_width": 120,
        "brick_height": 60,
        "mortar_chamfer": 5,
        "offset_x": 0,
        "offset_y": 0,
        "offset_z": 0,
        "row_repetition": 4,
        "tile_width": 4,
        "bond_pattern": "flemish",
        "file_name": "stretcher_v1",
        "export_formats": ["step", "stl"],
    }

    obj, created = Assembly.objects.get_or_create(name="stretcher_v1", model_type="tile", defaults={"metadata": tile_metadata})

    if created:
        print(f"✅ Added Tile Configuration: {obj.name}")
    else:
        print(f"🔄 Tile Configuration {obj.name} already exists. Skipping...")

if __name__ == "__main__":
    print("🚀 Seeding NMRA Standards, Parameters, and Tile Generator Settings into the database...")
    seed_nmra_standards()
    seed_parameters()
    seed_tile_generator_settings()
    print("✅ Database seeding complete!")
