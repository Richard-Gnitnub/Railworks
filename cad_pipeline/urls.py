from django.urls import path
from cad_pipeline.admin.admin_views import download_exported_file

app_name = "cad_pipeline"

urlpatterns = [
    path("exported-file/<int:file_id>/download/", download_exported_file, name="exportedfile_download"),
]
