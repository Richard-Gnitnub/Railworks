from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from resources.api.api import api  # Ensure API is correctly imported

def redirect_to_docs(request):
    """Redirects the root URL to the API documentation."""
    return HttpResponseRedirect("/api/docs")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # Mount the API
    path("", redirect_to_docs),  # ✅ Redirect "/" to "/api/docs"
]