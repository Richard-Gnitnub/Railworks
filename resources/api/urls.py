from django.urls import path
from resources.api.api import api

path("", api.urls),
