from django import forms
from django.contrib.auth.models import User

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "assigned_to", "priority"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)

        # Restrict the assigned_to field based on the user's role
        if user:
            if user.is_superuser:
                # Superusers can assign tasks to any user
                self.fields["assigned_to"].queryset = User.objects.all()
            else:
                # Non-superusers can only assign tasks to themselves
                self.fields["assigned_to"].queryset = User.objects.filter(id=user.id)
                self.fields[
                    "assigned_to"
                ].initial = user  # Set the default value to the current user
