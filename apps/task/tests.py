from django.contrib.auth import get_user_model
from django.test import TestCase

from ..task.models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(
            username="testuser",
            email="test@test.com",
        )
        user.set_password("1234")
        user.save()
        Task.objects.create(
            name="test task #1",
            description="Test description",
            creator=user,
        )
        Task.objects.create(
            name="test task #2",
            description="Test description 2",
            creator=user,
        )

    def test_state_transition(self):
        task1 = Task.objects.first()
        task1.mark_done()
        task1.save()
        task2 = Task.objects.last()
        self.assertEqual(task1.state, Task.State.DONE)
        self.assertEqual(task2.state, Task.State.TODO)
