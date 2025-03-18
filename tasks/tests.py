from django.contrib.auth.models import User
from django.test import TestCase

from .models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            assigned_to=self.user,
            created_by=self.user,
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
