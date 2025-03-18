from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import Task


# Home or Login Page (First Page)
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("task_list")  # Redirect to task list after login
    else:
        form = AuthenticationForm()
    return render(request, "tasks/login.html", {"form": form})


# Signup Page
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            messages.success(request, "Account created successfully!")
            return redirect("task_list")  # Redirect to task list after signup
    else:
        form = UserCreationForm()
    return render(request, "tasks/signup.html", {"form": form})


# Task List (Accessible after login)
@login_required
def task_list(request):
    if request.user.is_staff:
        tasks = Task.objects.filter(assigned_to=request.user)
    else:
        tasks = Task.objects.filter(created_by=request.user)
    return render(request, "task_list.html", {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)  # Pass the user to the form
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            if request.user.is_staff:
                task.assigned_to = (
                    request.user
                )  # Staff can only create tasks for themselves
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect("task_list")
    else:
        form = TaskForm(user=request.user)  # Pass the user to the form
    return render(request, "tasks/create_task.html", {"form": form})


# Assign Task (Only for superusers)
@login_required
def assign_task(request):
    if request.user.is_superuser:  # Only admin can assign tasks
        if request.method == "POST":
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.created_by = request.user
                task.save()
                messages.success(request, "Task assigned successfully!")
                return redirect("task_list")
        else:
            form = TaskForm()
        return render(request, "tasks/assign_task.html", {"form": form})
    else:
        messages.error(request, "You do not have permission to assign tasks.")
        return redirect("task_list")


# Logout
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")  # Redirect to login page after logout


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, "task_detail.html", {"task": task})


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/update_task.html", {"form": form})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user.is_superuser:
        task.delete()
        messages.success(request, "Task deleted successfully!")
    else:
        messages.error(request, "You do not have permission to delete this task.")
    return redirect("task_list")


@login_required
def change_priority(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        new_priority = request.POST.get("priority")
        task.priority = new_priority
        task.save()
        messages.success(request, "Priority updated successfully!")
        return redirect("task_list")


@login_required
def change_assigned(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    users = User.objects.all()  # Get all users
    if request.method == "POST":
        new_assigned_to_id = request.POST.get("assigned_to")
        new_assigned_to = get_object_or_404(User, id=new_assigned_to_id)
        task.assigned_to = new_assigned_to
        task.save()
        messages.success(request, "Assigned user updated successfully!")
        return redirect("task_list")
    return render(request, "tasks/change_assigned.html", {"task": task, "users": users})
