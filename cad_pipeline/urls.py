from django.urls import path
from cad_pipeline.api import api  # Import API entry point

urlpatterns = [
    path("api/", api.urls),  # Registers all API routes under `/api/`
]
