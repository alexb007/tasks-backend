from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class AuthTestCase(APITestCase):
    username = 'test'
    password = 'Tsd2@1341'

    def api_authentication(self):
        response = self.client.post(
            "/api-auth/jwt/create", data={
                "username": self.username, "password": self.password
            }
        )
        self.assertEqual(response.status_code, 200)
        self.token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def create_user(self):
        response = self.client.post(
            "/api-auth/users/", data={
                "username": self.username,
                "password": self.password,
            }
        )
        self.assertEqual(response.status_code, 201)
        return response.json()['id']

    def get_user(self):
        response = self.client.get(
            '/api-auth/users/me/',
        )
        self.assertEqual(response.status_code, 200)

    def edit_user(self, user_id):
        response = self.client.put(
            f'/api-auth/users/{user_id}/',
            data={
                'email': 'test@mail.com',
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_auth(self):
        user_id = self.create_user()
        self.api_authentication()
        self.get_user()
        self.edit_user(user_id)
