import os
import cadquery as cq
from io import BytesIO
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.cache import cache
from django.core.files.base import ContentFile
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.cad_engine.generate_component import generate_component  # ✅ Direct import

EXPORT_DIR = "media/exports/"
file_storage = FileSystemStorage(location=EXPORT_DIR)

class ExportedFile(models.Model):
    """
    Stores generated CAD models for retrieval and downloading.
    """
    component = models.ForeignKey(
        Assembly,
        on_delete=models.CASCADE,
        related_name="exports"
    )
    file = models.FileField(storage=file_storage, upload_to="models/")
    file_format = models.CharField(
        max_length=10,
        choices=[("stl", "STL"), ("step", "STEP")]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.component.name} ({self.file_format})"

    def save(self, *args, **kwargs):
        """
        Save method updates cache.
        """
        super().save(*args, **kwargs)
        cache.set(f"exported_file_{self.id}", self)  # ✅ Cache this export

    def delete(self, *args, **kwargs):
        """
        Ensure file deletion from storage and clear cache when entry is deleted.
        """
        if os.path.exists(self.file.path):
            os.remove(self.file.path)
        cache.delete(f"exported_file_{self.id}")  # ✅ Clear cache on delete
        super().delete(*args, **kwargs)

    @classmethod
    def get_cached_export(cls, export_id):
        """
        Retrieves the cached exported file or fetches from the database.
        """
        cache_key = f"exported_file_{export_id}"
        cached_export = cache.get(cache_key)
        if cached_export:
            return cached_export
        
        exported_file = cls.objects.get(id=export_id)
        cache.set(cache_key, exported_file, timeout=86400)  # ✅ Cache for 24 hours
        return exported_file

    @classmethod
    def generate_and_store(cls, component, file_format="stl"):
        """
        Generates a CAD model dynamically and stores it securely in the database.
        """
        cache_key = f"exported_component_{component.id}_{file_format}"

        # Check cache first
        cached_export = cache.get(cache_key)
        if cached_export:
            return cached_export

        # Generate the 3D model
        model = generate_component(component)

        file_buffer = BytesIO()

        if file_format == "stl":
            cq.exporters.export(model, file_buffer, "STL")
        elif file_format == "step":
            cq.exporters.export(model, file_buffer, "STEP")
        else:
            raise ValueError("Unsupported file format")

        # Save to database and storage
        exported_file = cls.objects.create(component=component, file_format=file_format)
        exported_file.file.save(f"{component.name.lower().replace(' ', '_')}.{file_format}",
                                ContentFile(file_buffer.getvalue()))

        # Cache the exported file
        cache.set(cache_key, exported_file, timeout=86400)  # ✅ Cache for 24 hours

        return exported_file
