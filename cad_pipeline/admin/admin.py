from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.models.exported_file import ExportedFile

@admin.register(Assembly)
class AssemblyAdmin(MPTTModelAdmin):
    """
    Enables hierarchical view of assemblies in Django Admin.
    """
    list_display = ("name", "type", "parent")
    search_fields = ("name", "type")
    list_filter = ("type",)
    ordering = ("name",)

@admin.register(ExportedFile)
class ExportedFileAdmin(admin.ModelAdmin):
    """
    Enables viewing and downloading of exported CAD files.
    """
    list_display = ("component", "file_format", "created_at")
    search_fields = ("component__name",)
    list_filter = ("file_format", "created_at")
