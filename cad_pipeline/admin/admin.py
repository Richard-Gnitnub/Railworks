from django.contrib import admin
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.models.exported_file import ExportedFile
from cad_pipeline.models.nmra_standard import NMRAStandard
from cad_pipeline.models.parameter import Parameter

# Optional: Define a base admin for soft-deletable models
class SoftDeleteAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_deleted", "created_at")
    list_filter = ("is_deleted",)
    search_fields = ("name",)
    actions = ["restore_records"]

    def get_queryset(self, request):
        """Exclude soft-deleted records by default"""
        return super().get_queryset(request).filter(is_deleted=False)

    @admin.action(description="Restore selected records")
    def restore_records(self, request, queryset):
        queryset.update(is_deleted=False)


# Register models
@admin.register(Assembly)
class AssemblyAdmin(SoftDeleteAdmin):
    list_display = ("id", "name", "model_type", "nmra_standard", "is_deleted", "created_at")
    list_filter = ("model_type", "is_deleted")
    search_fields = ("name", "metadata")


@admin.register(ExportedFile)
class ExportedFileAdmin(admin.ModelAdmin):
    list_display = ("id", "assembly", "file_name", "file_format", "generated_at")
    search_fields = ("file_name", "assembly__name", "file_format")
    list_filter = ("file_format", "generated_at")
    readonly_fields = ("assembly", "file_name", "file_path", "file_format", "generated_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(NMRAStandard)
class NMRAStandardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "scale_ratio", "gauge_mm", "rail_profile")
    search_fields = ("name",)


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parameter_type", "value")
    list_filter = ("parameter_type",)
    search_fields = ("name", "value")
