from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin
from cad_pipeline.models.assembly import Assembly
from cad_pipeline.models.exported_file import ExportedFile
from cad_pipeline.models.nmra_standard import NMRAStandard
from cad_pipeline.cad_engine.globals.cache_manager import is_cached

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
    list_display = ("component", "file_format", "created_at", "download_link", "cache_status")
    search_fields = ("component__name", "file_name")
    list_filter = ("file_format", "created_at")

    def download_link(self, obj):
        """
        Generates a secure download link for the exported file in Django Admin.
        Uses the correct reverse function to avoid `NoReverseMatch`.
        """
        try:
            url = reverse("admin:cad_pipeline_exportedfile_download", args=[obj.id])
            return format_html('<a href="{}" download>⬇️ Download</a>', url)
        except Exception:
            return "⚠️ URL Not Found"

    download_link.short_description = "Download"

    def cache_status(self, obj):
        """
        Displays whether the file is currently cached.
        """
        cached = is_cached(obj.file_name)  # ✅ Fixed function call (only 1 argument now)
        return format_html(
            '<span style="color:{};">{}</span>',
            "green" if cached else "red",
            "✅ Cached" if cached else "❌ Not Cached"
        )

    cache_status.short_description = "Cache Status"

@admin.register(NMRAStandard)
class NMRAStandardAdmin(admin.ModelAdmin):
    """
    Enables viewing and management of NMRA standards.
    """
    list_display = ("name", "scale_ratio", "gauge_mm", "rail_profile")
    search_fields = ("name",)
    ordering = ("name",)
