from django.db import models
from django.core.cache import cache
from mptt.models import MPTTModel, TreeForeignKey

class Assembly(MPTTModel):
    """
    Stores hierarchical structures such as bricks, tiles, walls, and buildings.
    Uses MPTT for parent-child relationships.
    """
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(
        max_length=50,
        choices=[
            ("brick", "Brick"),
            ("brick_tile", "Brick Tile"),
            ("wall", "Wall"),
            ("building", "Building"),
            ("door", "Door"),
            ("roof", "Roof")
        ]
    )

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return f"{self.name} ({self.type})"

    def save(self, *args, **kwargs):
        """
        Save method updates database and refreshes cache.
        """
        super().save(*args, **kwargs)
        cache.set(f"assembly_{self.id}", self)  # Cache the instance

    def delete(self, *args, **kwargs):
        """
        Custom delete method: clears cache and removes child structures.
        """
        cache.delete(f"assembly_{self.id}")
        super().delete(*args, **kwargs)

    @classmethod
    def get_cached(cls, assembly_id):
        """
        Retrieves the cached assembly if available, otherwise fetches from the DB.
        """
        cached_assembly = cache.get(f"assembly_{assembly_id}")
        if cached_assembly:
            return cached_assembly
        assembly = cls.objects.get(id=assembly_id)
        cache.set(f"assembly_{assembly_id}", assembly)
        return assembly
