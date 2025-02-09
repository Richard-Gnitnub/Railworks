from django.contrib import admin
from django.urls import path
from cad_pipeline.api import api  # Import API entry point
from cad_pipeline.admin.admin_views import download_exported_file  # ✅ Import the correct view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/exported-file/<int:file_id>/download/", download_exported_file, name="admin:cad_pipeline_exportedfile_download"),  # ✅ Corrected URL pattern
    path("api/", api.urls),  # Registers all API routes under `/api/`
]
