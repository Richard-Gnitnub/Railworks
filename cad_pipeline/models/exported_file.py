from django.db import models
from django.utils.timezone import now
from cad_pipeline.models.assembly import Assembly


class ExportedFile(models.Model):
    """
    Stores exported CAD files (e.g., STEP, STL) **in the database only**.
    Caching is now handled by `cache_manager.py` for modularity.
    """
    component = models.ForeignKey(Assembly, on_delete=models.CASCADE, related_name="exports")
    file_format = models.CharField(max_length=10, choices=[("step", "STEP"), ("stl", "STL")])
    file_name = models.CharField(max_length=255)  # ✅ Stores the filename dynamically
    file_data = models.BinaryField()  # ✅ Stores the actual CAD file content in the database
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.component.name} ({self.file_format})"

    @classmethod
    def generate_filename(cls, component, file_format):
        """
        Generates a dynamic filename based on the component's MPTT hierarchy.
        Example: "brick_geometry_generate_flemish_brick_tile.step"
        """
        hierarchy_path = "_".join(component.get_ancestors(include_self=True).values_list("name", flat=True))
        return f"{hierarchy_path.lower().replace(' ', '_')}.{file_format}"

    @classmethod
    def store_exported_file(cls, component, file_format, file_data):
        """
        Stores an exported CAD file **in the database**.
        Calls `cache_manager` to handle caching.
        """
        file_name = cls.generate_filename(component, file_format)

        # ✅ Store in the database
        exported_file, created = cls.objects.update_or_create(
            component=component,
            file_format=file_format,
            defaults={
                "file_name": file_name,
                "file_data": file_data,
                "created_at": now(),
            },
        )

        print(f"✅ Stored Exported File: {file_name} (Updated: {not created})")

        # ✅ Call cache manager to cache the file
        from cad_pipeline.cad_engine.globals.cache_manager import cache_exported_file
        cache_exported_file(exported_file)

        return exported_file
