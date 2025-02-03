from django.db import models
from .nmra_standard import NMRAStandard  # Correct relative import

class Assembly(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)  # Indexed for unique name lookups
    model_type = models.CharField(
        max_length=50, 
        choices=[("track", "Track"), ("wall", "Wall"), ("building", "Building")],
        db_index=True  # Useful for filtering by type
    )
    nmra_standard = models.ForeignKey(
        NMRAStandard, on_delete=models.SET_NULL, null=True, db_index=True  # ForeignKey lookups benefit from indexing
    )
    metadata = models.JSONField(default=dict)  # Not indexed as JSON fields are usually not used for filtering
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Indexed for ordering by creation date

    is_deleted = models.BooleanField(default=False, db_index=True)  # Indexed for soft deletion filtering

    class Meta:
        indexes = [
            models.Index(fields=["model_type", "created_at"], name="type_created_idx"),  # Multi-column index for filtering/sorting
        ]

    def __str__(self):
        return f"{self.model_type}: {self.name}"
