from django.contrib import admin
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.models.nmra_standard import NMRAStandard
from cad_pipeline.models.parameter import Parameter
from cad_pipeline.models.exported_file import ExportedFile

# ✅ Soft Deletion Admin Base Class
class SoftDeleteAdmin(admin.ModelAdmin):
    """Custom admin to support soft deletion"""
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

# ✅ Assembly Admin (With Soft Delete)
@admin.register(Assembly)
class AssemblyAdmin(SoftDeleteAdmin):
    """Admin view for managing Assemblies"""
    list_display = ("id", "name", "model_type", "nmra_standard", "is_deleted", "created_at")
    list_filter = ("model_type", "is_deleted")
    search_fields = ("name", "metadata")

# ✅ NMRA Standard Admin
@admin.register(NMRAStandard)
class NMRAStandardAdmin(admin.ModelAdmin):
    """Admin view for NMRA Standards"""
    list_display = ("id", "name", "scale_ratio", "gauge_mm", "rail_profile")
    search_fields = ("name",)

# ✅ Parameter Admin
@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    """Admin view for managing Parameters"""
    list_display = ("id", "name", "parameter_type", "value")
    list_filter = ("parameter_type",)
    search_fields = ("name", "value")

# ✅ Exported File Admin (Read-Only Logs)
@admin.register(ExportedFile)
class ExportedFileAdmin(admin.ModelAdmin):
    """Admin view for tracking exported files"""
    list_display = ("id", "assembly", "file_name", "file_format", "generated_at")
    search_fields = ("file_name", "assembly__name", "file_format")
    list_filter = ("file_format", "generated_at")
    readonly_fields = ("assembly", "file_name", "file_path", "file_format", "generated_at")

    def has_add_permission(self, request):
        """Prevent admins from manually adding exported files"""
        return False  # Prevents new records from being added manually

    def has_change_permission(self, request, obj=None):
        """Prevent modification of exported file records"""
        return False  # Prevents editing existing records

    def has_delete_permission(self, request, obj=None):
        """Prevent manual deletion of exported files"""
        return False  # Protects logs from deletion
