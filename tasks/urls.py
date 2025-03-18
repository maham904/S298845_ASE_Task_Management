from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.user_login, name="login"),  # Login page as the first page
    path("signup/", views.signup, name="signup"),  # Signup page
    path(
        "tasks/", views.task_list, name="task_list"
    ),  # Task list (accessible after login)
    path("tasks/create/", views.create_task, name="create_task"),  # Create task
    path(
        "tasks/assign/", views.assign_task, name="assign_task"
    ),  # Assign task (for superusers)
    path("logout/", views.user_logout, name="logout"),  # Logout
    path("<int:task_id>/", views.task_detail, name="task_detail"),
    path("<int:task_id>/update/", views.update_task, name="update_task"),
    path("tasks/<int:task_id>/delete/", views.delete_task, name="delete_task"),
    path(
        "tasks/<int:task_id>/change-priority/",
        views.change_priority,
        name="change_priority",
    ),
    path(
        "tasks/<int:task_id>/change-assigned/",
        views.change_assigned,
        name="change_assigned",
    ),
]
