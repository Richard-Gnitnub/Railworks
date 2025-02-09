import os
from django.db import models
from django.core.files.base import ContentFile
from django.core.cache import cache
from cad_pipeline.models.assembly import Assembly

class ExportedFile(models.Model):
    """
    Stores exported CAD models for retrieval and downloading.
    """
    component = models.ForeignKey(
        Assembly,
        on_delete=models.CASCADE,
        related_name="exports"
    )
    file = models.FileField(upload_to="exports/")
    file_format = models.CharField(
        max_length=10,
        choices=[("stl", "STL"), ("step", "STEP")]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Ensure proper caching after storing in the database.
        """
        super().save(*args, **kwargs)
        cache.set(f"exported_file_{self.id}", self.file, timeout=86400)

    @classmethod
    def store_exported_file(cls, component, file_format, file_data):
        """
        Stores an exported CAD model securely in the database.
        """
        exported_file, _ = cls.objects.get_or_create(
            component=component,
            file_format=file_format
        )
        exported_file.file.save(
            f"{component.name.lower().replace(' ', '_')}.{file_format}",
            ContentFile(file_data)  # ✅ FIXED: Use ContentFile for binary storage
        )
        return exported_file
