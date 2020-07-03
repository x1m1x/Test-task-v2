from rest_framework.test import APITestCase, APIClient

from django.contrib.auth.hashers import make_password

from rest_framework import status

from django.contrib.auth.models import User


class ImagesListTestCase(APITestCase):
    def setUp(self):
        self.data = {
            'username': 'username',
            'password': 'password'
        }

    def test_images_list(self):
        user = User.objects.create(username="username", password=make_password("password"))

        response = self.client.post('/api/token', data=self.data)
        token = response.json()['access']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api', data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateImageTestCase(APITestCase):
    def setUp(self):
        self.data = {
            'description': 'image',
            'image_url': 'https://127.0.0.1:8000',
            'id': 123
        }
    def test_image_upload(self):
        response = self.client.post('/api/image/create', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookmarkTestCase(APITestCase):
    def test_bookmark(self):
        response = self.client.get('/api/image/36717/add_to_bookmark')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get('/api/bookmark')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetAccessRefreshTokensTestCase(APITestCase):
    def setUp(self):
        self.data = {
            'username': 'username',
            'password': 'password'
        }

    def test_get_access_refresh_token(self):
        user = User.objects.create(username="username", password=make_password("password"))

        response = self.client.post('/api/token', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetRefreshTokenTestCase(APITestCase):
    def setUp(self):
        self.data = {
            'username': 'username',
            'password': 'password'
        }

    def test_get_refresh_token(self):
        user = User.objects.create(username="username", password=make_password("password"))

        response = self.client.post('/api/token', data=self.data)
        refresh_token = response.json()['refresh']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post('/api/token/refresh', data={'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RegistrationTestCase(APITestCase):
    def setUp(self):
        self.data = {
            'username': 'username',
            'password': 'password'
        }

    def test_registration(self):
        response = self.client.post('/api/register', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class NotFoundTestCase(APITestCase):
    def test_not_found(self):
        response = self.client.get('/api/fsdjfkasj')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
