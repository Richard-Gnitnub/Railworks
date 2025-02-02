from django.db import models
from .assembly import Assembly  # Correct relative import

class ExportedFile(models.Model):
    assembly = models.ForeignKey(Assembly, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=512)
    file_format = models.CharField(max_length=10, choices=[("step", "STEP"), ("stl", "STL")])
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assembly.name} - {self.file_format} ({self.generated_at})"
