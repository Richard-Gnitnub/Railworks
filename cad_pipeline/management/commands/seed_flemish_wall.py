import logging
from django.core.management.base import BaseCommand
from cad_pipeline.models.assembly import Assembly

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class Command(BaseCommand):
    help = "Seeds the generate_flemish_wall assembly with predefined parameters."

    def handle(self, *args, **kwargs):
        """Populates the `generate_flemish_wall` Assembly with JSON parameters."""
        wall_data = {
            "name": "generate_flemish_wall",
            "parameters": {
                "cutouts": [  # ✅ Fully dynamic cutout parameters
                    {"x": 200, "z": 150, "width": 50, "height": 100, "depth": 150},
                    {"x": 600, "z": 150, "width": 50, "height": 100, "depth": 150},
                    {"x": 400, "z": 350, "width": 100, "height": 200, "depth": 250}
                ],
                "apply_boundary_logic": False,  # ✅ Placeholder for boundary logic
            }
        }

        try:
            obj, created = Assembly.objects.get_or_create(
                name=wall_data["name"], defaults={"parameters": wall_data["parameters"]}
            )

            if created:
                logging.info(f"✅ Added Assembly: {wall_data['name']}")
            else:
                logging.info(f"🔄 Assembly {wall_data['name']} already exists. Updating parameters...")
                obj.parameters = wall_data["parameters"]
                obj.save()
                logging.info(f"✅ Updated {wall_data['name']} parameters!")

            logging.info("✅ Flemish Wall Seeding Complete!")

        except Exception as e:
            logging.error(f"❌ ERROR: Failed to seed database: {e}")
