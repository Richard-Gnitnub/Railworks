from django.core.management.base import BaseCommand
from cad_pipeline.models.nmra_standard import NMRAStandard

class Command(BaseCommand):
    help = "Seeds the NMRA Standards into the database."

    def handle(self, *args, **kwargs):
        nmra_data = [
            {"name": "HO", "scale_ratio": 1/87.1, "gauge_mm": 16.5, "rail_profile": "Code 83"},
            {"name": "N", "scale_ratio": 1/160, "gauge_mm": 9, "rail_profile": "Code 55"},
            {"name": "O", "scale_ratio": 1/48, "gauge_mm": 32, "rail_profile": "Code 148"},
        ]

        for data in nmra_data:
            nmra, created = NMRAStandard.objects.get_or_create(name=data["name"], defaults=data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added NMRA Standard: {nmra.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"NMRA Standard '{nmra.name}' already exists."))

        self.stdout.write(self.style.SUCCESS("✅ NMRA Standards seeding completed!"))
