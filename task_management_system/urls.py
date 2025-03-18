from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin URLs
    path("", include("tasks.urls")),  # Include tasks app URLs
]
