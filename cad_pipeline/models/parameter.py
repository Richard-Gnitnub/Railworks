from django.db import models
from django.core.exceptions import ValidationError
from django.core.cache import cache
from cad_pipeline.models.assembly import Assembly  # ✅ Correct Import

class Parameter(models.Model):
    """
    Stores dynamic parameters for assemblies with enforced constraints.
    """
    assembly = models.ForeignKey(
        Assembly,
        on_delete=models.CASCADE,
        related_name="parameters"
    )
    key = models.CharField(max_length=255)
    value = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.assembly.name} - {self.key}: {self.value}"

    def clean(self):
        """
        Enforces validation on stored parameters.
        """
        errors = {}

        if self.assembly.type == "wall":
            if self.key == "height":
                if not isinstance(self.value, (int, float)) or self.value < 500 or self.value > 5000:
                    errors["height"] = "Wall height must be between 500mm and 5000mm."

            if self.key == "width":
                if not isinstance(self.value, (int, float)) or self.value < 500 or self.value > 10000:
                    errors["width"] = "Wall width must be between 500mm and 10000mm."

        if self.assembly.type == "brick_wall":
            if self.key == "brick_pattern":
                allowed_patterns = ["Flemish Bond", "Running Bond"]
                if self.value not in allowed_patterns:
                    errors["brick_pattern"] = f"Invalid brick pattern. Allowed values: {allowed_patterns}"

        if self.assembly.type == "house":
            if self.key == "num_floors":
                if not isinstance(self.value, int) or self.value < 1 or self.value > 10:
                    errors["num_floors"] = "Number of floors must be between 1 and 10."

        # Raise error if validation fails
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Validate before saving and cache updated parameters.
        """
        self.clean()  # ✅ Validate before saving
        super().save(*args, **kwargs)
        self.update_cache()

    def delete(self, *args, **kwargs):
        """
        Remove cached parameters on delete.
        """
        super().delete(*args, **kwargs)
        self.update_cache()

    def update_cache(self):
        """
        Updates the cache for the associated assembly's parameters.
        """
        cache.set(f"parameters_{self.assembly.id}", list(self.assembly.parameters.all()), timeout=86400)  # ✅ Cache for 24 hours

    @classmethod
    def get_cached_parameters(cls, assembly):
        """
        Retrieves cached parameters or fetches from the database.
        """
        cache_key = f"parameters_{assembly.id}"
        cached_params = cache.get(cache_key)

        if cached_params:
            return cached_params
        
        params = list(assembly.parameters.all())
        cache.set(cache_key, params, timeout=86400)  # ✅ Cache for 24 hours
        return params
