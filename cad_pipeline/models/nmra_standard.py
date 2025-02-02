from django.db import models

class NMRAStandard(models.Model):
    name = models.CharField(max_length=50, unique=True)  # "HO Scale"
    scale_ratio = models.FloatField()  # 1:87.1
    gauge_mm = models.FloatField()  # 16.5mm
    clearance_mm = models.JSONField(default=dict)  # Stores all NMRA-defined clearances
    rail_profile = models.CharField(max_length=50)  # "Code 75 Bullhead"

    def __str__(self):
        return f"{self.name} ({self.gauge_mm}mm)"
