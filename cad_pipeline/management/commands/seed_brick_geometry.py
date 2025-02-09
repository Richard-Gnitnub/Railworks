from django.core.management.base import BaseCommand
from cad_pipeline.models.assembly import Assembly

class Command(BaseCommand):
    help = "Seeds standard brick geometry into the database."

    def handle(self, *args, **kwargs):
        brick_data = [
            {
                "name": "brick_geometry",
                "type": "brick",
                "parameters": {
                    "brick_length": 215,
                    "brick_width": 102.5,
                    "brick_height": 65,
                    "mortar_chamfer": 10
                }
            }
        ]

        for data in brick_data:
            brick, created = Assembly.objects.get_or_create(name=data["name"], type=data["type"], defaults={"parameters": data["parameters"]})
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Added Brick Geometry: {brick.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Brick Geometry '{brick.name}' already exists."))

        self.stdout.write(self.style.SUCCESS("✅ Brick Geometry Seeding Completed!"))
