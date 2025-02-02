from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from cad_pipeline.api import api  # ✅ Import Django Ninja API

def redirect_to_docs(request):
    """Redirects `/` to Swagger UI at `/api/docs/`."""
    return redirect("/api/docs/")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # ✅ Registers Django Ninja API
    path("", redirect_to_docs),  # ✅ Redirects `/` to `/api/docs/`
]
