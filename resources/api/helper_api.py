from ninja import Router
from django.http import JsonResponse
import os

router = Router(tags=["Helpers"])

@router.get("/check-media-folder", summary="Check if media folder exists")
def check_media_folder(request):
    """
    Checks if the media directory exists.
    """
    media_path = "media/"
    exists = os.path.exists(media_path)
    
    return JsonResponse({"media_folder_exists": exists}, status=200)
