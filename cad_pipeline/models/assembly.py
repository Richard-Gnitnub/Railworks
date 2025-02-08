import os
from django.db import models
from django.core.cache import cache
from mptt.models import MPTTModel, TreeForeignKey

class Assembly(MPTTModel):
    """
    Stores hierarchical structures such as houses, walls, fences, and tracks.
    Uses MPTT for parent-child relationships and caching.
    """
    name = models.CharField(max_length=255, unique=True)  # ✅ Keep unique constraint to prevent duplicates
    type = models.CharField(
        max_length=50,
        choices=[
            ("house", "House"),
            ("wall", "Wall"),
            ("roof", "Roof"),
            ("brick_wall", "Brick Wall"),
            ("wooden_fence", "Wooden Fence"),
            ("track", "Track"),
            ("rail", "Rail"),
            ("sleeper", "Sleeper"),
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
        Custom save method:
        - If an assembly with the same name and type exists, update it.
        - Otherwise, create a new entry.
        - Refreshes cache after saving.
        """
        existing = Assembly.objects.filter(name=self.name, type=self.type).first()

        if existing:
            # ✅ Update existing record instead of creating a new one
            self.id = existing.id
            kwargs["force_update"] = True
            print(f"🔄 Updating existing assembly: {self.name} ({self.type})")
        else:
            print(f"🆕 Creating new assembly: {self.name} ({self.type})")

        super().save(*args, **kwargs)

        # ✅ Cache the updated assembly
        cache.set(f"assembly_{self.id}", self)
        cache.delete("all_assemblies")  # ✅ Clear list cache

    @classmethod
    def get_cached(cls, assembly_id):
        """
        Retrieves the cached assembly if available, otherwise fetches from the DB.
        """
        cache_key = f"assembly_{assembly_id}"
        cached_assembly = cache.get(cache_key)
        if cached_assembly:
            return cached_assembly
        
        assembly = cls.objects.get(id=assembly_id)
        cache.set(cache_key, assembly, timeout=86400)  # ✅ Cache for 24 hours
        return assembly

    @classmethod
    def get_all_cached(cls):
        """
        Retrieves all assemblies from cache or fetches from the database.
        """
        cache_key = "all_assemblies"
        cached_assemblies = cache.get(cache_key)

        if cached_assemblies:
            return cached_assemblies
        
        assemblies = list(cls.objects.all())
        cache.set(cache_key, assemblies, timeout=86400)  # ✅ Cache for 24 hours
        return assemblies
