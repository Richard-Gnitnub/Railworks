from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from cad_pipeline.models.exported_file import ExportedFile

def download_exported_file(request, file_id):
    """
    Serves an exported file for download from the database.
    """
    exported_file = get_object_or_404(ExportedFile, id=file_id)
    
    response = HttpResponse(exported_file.file_data, content_type="application/octet-stream")
    response["Content-Disposition"] = f"attachment; filename={exported_file.file_name}"
    
    return response
