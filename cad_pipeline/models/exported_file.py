from django.db import models
from .assembly import Assembly  # Correct relative import

class ExportedFile(models.Model):
    assembly = models.ForeignKey(Assembly, on_delete=models.CASCADE, db_index=True)  # Indexed for ForeignKey lookups
    file_name = models.CharField(max_length=255, db_index=True)  # Indexed for quick lookups by name
    file_path = models.CharField(max_length=512)  # Not indexed as file paths are usually not filtered or searched
    file_format = models.CharField(
        max_length=10,
        choices=[("step", "STEP"), ("stl", "STL")],
        db_index=True  # Indexed for filtering by format
    )
    generated_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Indexed for sorting/filtering by date

    def __str__(self):
        return f"{self.assembly.name} - {self.file_format} ({self.generated_at})"
