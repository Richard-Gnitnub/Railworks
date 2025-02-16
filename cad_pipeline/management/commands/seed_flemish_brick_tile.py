from django.core.management.base import BaseCommand
from cad_pipeline.models.assembly import Assembly

class Command(BaseCommand):
    help = "Seeds the Flemish Brick Tile Generator into the database."

    def handle(self, *args, **kwargs):
        tile_data = [
            {
                "name": "generate_flemish_brick_tile",
                "type": "brick_tile",
                "parameters": {
                    "tile_width": 8,
                    "row_repetition": 8,
                    "bond_pattern": "flemish"
                }
            }
        ]

        for data in tile_data:
            tile, created = Assembly.objects.get_or_create(name=data["name"], type=data["type"], defaults={"parameters": data["parameters"]})
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Added Tile Generator: {tile.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Tile Generator '{tile.name}' already exists."))

        self.stdout.write(self.style.SUCCESS("✅ Flemish Brick Tile Generator Seeding Completed!"))
