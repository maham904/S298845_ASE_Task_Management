from django.contrib import admin
from django.urls import path, include
from tasks import views  # Correct import statement

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path('', views.home, name='home'),  # Example: Map root path to a home view
]