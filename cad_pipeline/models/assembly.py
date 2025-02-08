from django.db import models
from django.core.cache import cache
from .nmra_standard import NMRAStandard  # Correct relative import

class Assembly(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)  # Unique and indexed for fast lookups
    model_type = models.CharField(
        max_length=50, 
        choices=[("track", "Track"), ("wall", "Wall"), ("building", "Building")],
        db_index=True  # Indexed for filtering by model type
    )
    nmra_standard = models.ForeignKey(
        NMRAStandard, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="assemblies",
        db_index=True  # Ensures fast lookups for related NMRA standards
    )
    metadata = models.JSONField(default=dict)  # Stores CAD parameters (dimensions, materials, etc.)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Indexed for sorting by creation date
    updated_at = models.DateTimeField(auto_now=True, db_index=True)  # Tracks the last modification, indexed for filtering
    is_deleted = models.BooleanField(default=False, db_index=True)  # Soft delete flag for safer deletions

    class Meta:
        ordering = ["-created_at"]  # Default ordering by most recently created
        indexes = [
            models.Index(fields=["name"], name="assembly_name_idx"),
            models.Index(fields=["model_type"], name="assembly_type_idx"),
            models.Index(fields=["created_at"], name="assembly_created_at_idx"),
            models.Index(fields=["is_deleted"], name="assembly_is_deleted_idx"),
        ]  # Additional indexes for faster query performance

    def __str__(self):
        return f"{self.model_type}: {self.name}"

    def save(self, *args, **kwargs):
        """Invalidate cache when saving an updated Assembly"""
        cache_key = self.generate_cache_key()
        cache.delete(cache_key)
        super().save(*args, **kwargs)  # Call the parent save method

    def delete(self, *args, **kwargs):
        """Perform a soft delete by setting is_deleted flag"""
        self.is_deleted = True
        self.save(*args, **kwargs)

    def generate_cache_key(self):
        """
        Generates a unique cache key for the assembly instance.
        """
        return f"assembly:{self.id}"

    @classmethod
    def get_cached_assembly(cls, assembly_id):
        """
        Retrieve an Assembly from the cache if available.
        """
        cache_key = f"assembly:{assembly_id}"
        cached_assembly = cache.get(cache_key)
        if not cached_assembly:
            assembly = cls.objects.get(id=assembly_id)
            cache.set(cache_key, assembly, timeout=86400)  # Cache for 24 hours
            return assembly
        return cached_assembly
