from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class TaskTestCase(APITestCase):
    username1 = 'test1'
    username2 = 'test2'
    password = 'Tsd2@1341'

    def setUp(self):
        User = get_user_model()
        user = User.objects.create(
            username=self.username1,
            email="test@test.com",
        )
        user.set_password(self.password)
        user.save()
        self.user1 = user
        user2 = User.objects.create(
            username=self.username2,
            email="test@test.com",
        )
        user2.set_password(self.password)
        user2.save()
        self.user2 = user2

    def api_authentication(self):
        response = self.client.post(
            "/api-auth/jwt/create", data={
                "username": self.username1, "password": self.password
            }
        )
        self.assertEqual(response.status_code, 200)
        self.token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def create_task(self):
        response = self.client.post(
            "/api/v1/tasks/", data={
                "name": "test task",
                "description": "Task description",
            }
        )
        self.assertEqual(response.status_code, 201)
        return response.json()['id']

    def assign_task(self, task_id):
        response = self.client.patch(
            f"/api/v1/tasks/{task_id}/assign/", data={
                "user": self.user2.id,
            }
        )
        self.assertEqual(response.status_code, 200)

    def comment(self, task_id):
        response = self.client.post(
            f"/api/v1/tasks/{task_id}/comment/", data={
                "comment": "Test Comment",
            }
        )
        self.assertEqual(response.status_code, 200)

    def complete(self, task_id):
        response = self.client.patch(
            f"/api/v1/tasks/{task_id}/complete/"
        )
        self.assertEqual(response.status_code, 200)

    def test_task_endpoints(self):
        self.api_authentication()
        task_id = self.create_task()
        self.assign_task(task_id)
        self.comment(task_id)
        self.complete(task_id)

