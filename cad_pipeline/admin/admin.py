from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.models.exported_file import ExportedFile
from cad_pipeline.models.nmra_standard import NMRAStandard

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
    list_display = ("component", "file_format", "created_at", "download_file")
    search_fields = ("component__name",)
    list_filter = ("file_format", "created_at")

    def download_file(self, obj):
        """
        Provide a link to download the exported file.
        """
        # Assuming `file` is the field that stores the file URL
        if hasattr(obj, 'file') and obj.file:  
            return format_html(
                '<a href="{}" download>Download</a>',
                obj.file.url  # Ensure MEDIA_URL is configured correctly
            )
        return "No file available"

    download_file.short_description = "Download File"

@admin.register(NMRAStandard)
class NMRAStandardAdmin(admin.ModelAdmin):
    """
    Enables management of NMRA standards in Django Admin.
    """
    list_display = ("name", "scale_ratio", "gauge_mm", "rail_profile")
    search_fields = ("name", "rail_profile")
    list_filter = ("scale_ratio", "gauge_mm")
    ordering = ("name",)
