from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect

# Define the debug function
def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sentry-debug/', trigger_error),
    path('', lambda request: HttpResponseRedirect('/admin/')),  # Redirect root to /admin/
]
