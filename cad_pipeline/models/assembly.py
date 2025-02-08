from django.db import models, IntegrityError
from django.core.cache import cache
from .nmra_standard import NMRAStandard  # Correct relative import


class Assembly(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    model_type = models.CharField(
        max_length=50,
        choices=[("track", "Track"), ("wall", "Wall"), ("tile", "Tile"), ("building", "Building")],
        db_index=True
    )
    nmra_standard = models.ForeignKey(
        NMRAStandard,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assemblies",
        db_index=True
    )
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    version = models.PositiveIntegerField(default=1, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"], name="assembly_name_idx"),
            models.Index(fields=["model_type"], name="assembly_type_idx"),
            models.Index(fields=["created_at"], name="assembly_created_at_idx"),
            models.Index(fields=["is_deleted"], name="assembly_is_deleted_idx"),
        ]

    def __str__(self):
        return f"{self.model_type}: {self.name} v{self.version}"

    def save(self, *args, **kwargs):
        """Invalidate cache, update versioning, and save the instance."""
        cache_key = self.generate_cache_key()
        cached_data = cache.get(cache_key)

    # Debugging log
        print(f"🔄 Saving Assembly: {self.name} (v{self.version})")
        print(f"🔍 Cached Data Before Save: {cached_data}")

    # Increment version if metadata has changed
        if cached_data and cached_data.metadata != self.metadata:
            self.version += 1
            print(f"📈 Metadata changed, incrementing version to {self.version}")

        cache.delete(cache_key)  # Remove stale cache
        print(f"🗑️ Cache invalidated for {cache_key}")

        super().save(*args, **kwargs)  # Call the parent save method

    # Update cache with latest data
        cache.set(cache_key, self, timeout=86400)
        print(f"✅ New Assembly cached: {cache.get(cache_key)}")


    def delete(self, *args, **kwargs):
        """Perform a soft delete by setting is_deleted flag and clearing cache."""
        self.is_deleted = True
        self.save(*args, **kwargs)

    def generate_cache_key(self):
        """Generate a unique cache key for the assembly instance."""
        return f"assembly:{self.id}"

    @classmethod
    def get_cached_assembly(cls, assembly_id):
        """Retrieve an Assembly from cache or database."""
        cache_key = f"assembly:{assembly_id}"
        cached_assembly = cache.get(cache_key)
        if not cached_assembly:
            assembly = cls.objects.get(id=assembly_id)
            cache.set(cache_key, assembly, timeout=86400)
            return assembly
        return cached_assembly

    @classmethod
    def update_or_create_with_version(cls, name, model_type, metadata):
        """
        Update an assembly if it exists, otherwise create a new version.
        """
        try:
            assembly, created = cls.objects.get_or_create(
                name=name,
                model_type=model_type,
                defaults={"metadata": metadata}
            )
            if not created:
                # Increment version if an update is needed
                assembly.version += 1
                assembly.metadata = metadata
                assembly.save(update_fields=["version", "metadata", "updated_at"])
                cache.set(assembly.generate_cache_key(), assembly, timeout=86400)
            return assembly
        except IntegrityError:
            latest_version = cls.objects.filter(name=name, model_type=model_type).order_by("-version").first()
            new_version = latest_version.version + 1 if latest_version else 1
            assembly = cls.objects.create(
                name=name,
                model_type=model_type,
                metadata=metadata,
                version=new_version
            )
            cache.set(assembly.generate_cache_key(), assembly, timeout=86400)
            return assembly
