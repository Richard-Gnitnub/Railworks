from django.db import models
from .nmra_standard import NMRAStandard  # Correct relative import

class Assembly(models.Model):
    name = models.CharField(max_length=255, unique=True)  # "Warehouse Wall 3m x 2m"
    model_type = models.CharField(
        max_length=50, 
        choices=[("track", "Track"), ("wall", "Wall"), ("building", "Building")]
    )
    nmra_standard = models.ForeignKey(NMRAStandard, on_delete=models.SET_NULL, null=True)
    metadata = models.JSONField(default=dict)  # Stores CAD parameters (dimensions, materials)
    created_at = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.model_type}: {self.name}"
