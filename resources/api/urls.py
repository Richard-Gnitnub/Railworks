from django.urls import path
from resources.api import api  # Import main API instance (fixed import loop)

urlpatterns = [
    path("", api.urls),  # Mount Django Ninja API
]
