from django.contrib import admin
from django.urls import path, include
from cad_pipeline.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/", include("cad_pipeline.urls", namespace="cad_pipeline")),
    path("api/", api.urls),
]
