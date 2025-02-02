from django.db import models

class Parameter(models.Model):
    PARAMETER_TYPES = [
        ("bond_pattern", "Bond Pattern"),
        ("export_format", "Export Format"),
        ("tile_constraint", "Tile Constraint"),
    ]

    name = models.CharField(max_length=255, unique=True)  # e.g., "flemish", "step", "max_tile_width"
    value = models.JSONField(default=dict)  # Stores lists, dicts, or single values
    parameter_type = models.CharField(max_length=50, choices=PARAMETER_TYPES)

    def __str__(self):
        return f"{self.parameter_type}: {self.name}"
