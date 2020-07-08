from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Image

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.urls import reverse

import jwt


class SetUp:
    def setUp(self) :
        self.register_url = reverse("user_create_url")
        self.user_data = {
            "username": "test_user",
            "password": "123456789"
        }
        self.client.post(self.register_url,self.user_data)

        auth_url = reverse("token_obtain_pair_url")
        response = self.client.post(auth_url,{
            "username" : self.user_data.get("username") ,
            "password" : self.user_data.get("password")
        })
        self.access_token = response.data.get("access")
        self.refresh_token = response.data.get("refresh")

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.data = {}


# images
class ImagesListTestCase(SetUp, APITestCase):
    def test_dashboard(self):
        response = self.client.get('/api')
        self.assertEqual(len(response.json()), 80)

    def test_search_dashboard(self):
        response = self.client.get('/api?search=photo')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_limit_dashboard(self):
        response = self.client.get('/api?search=photo&limit=50')
        self.assertEqual(len(response.json()), 50)

    def test_dashboard_limit_less_80(self):
        response = self.client.get('/api?limit=50')
        self.assertEqual(len(response.json()), 50)

    def test_dashboard_limit_more_80(self):
        response = self.client.get('/api?limit=90')
        self.assertEqual(len(response.json()), 90)

    def test_dashboard_limit_equals_300(self):
        response = self.client.get('/api?limit=300')
        self.assertEqual(response.json(), {'detail': 'Bad request'})

    def test_limit_dashboard_invalid(self):
        response = self.client.get('/api?limit=photo')
        errors = {'detail': 'Bad request'}
        self.assertEqual(response.json(), errors)

class CreateImageTestCase(SetUp, APITestCase):
    def test_image_upload(self):
        self.data = {
            'description': 'image',
            'image_url': 'https://127.0.0.1:8000',
        }
        response = self.client.post('/api/image/create', data=self.data)
        self.assertEqual(response.json(), self.data)

        response = self.client.get('/api')
        last_item = response.json()[len(response.json())-1]
        image = Image.objects.get(description=self.data.get('description'))
        self.data['id'] = image.id
        self.assertEqual(last_item, self.data)

    def test_image_upload_second_time(self):
        self.data = {
            'description': 'image',
            'image_url': 'https://127.0.0.1:8000',
        }
        errors = {'image_url': ['Such image is already exist']}

        self.client.post('/api/image/create', data=self.data)
        response = self.client.post('/api/image/create', data=self.data)
        self.assertEqual(response.json(), errors)

    def test_image_upload_bad_request(self):
        self.data = {
            'description': '',
            'image_url': 'invalid_url',
        }
        errors = {'description': ['This field may not be blank.'], 'image_url': ['Enter a valid URL.']}

        response = self.client.post('/api/image/create', data=self.data)
        self.assertEqual(response.json(), errors)

class ImageDetailTestCase(SetUp, APITestCase):
    def test_api_image_detail(self):
        self.data = {
            'description': 'flight-landscape-nature-sky',
            'image_url': 'https://images.pexels.com/photos/36717/amazing-animal-beautiful-beautifull.jpg',
            'id': 36717
        }

        response = self.client.get(f"/api/image/36717")
        self.assertEqual(response.json(), self.data)

    def test_image_detail(self):
        self.data = {
            'description': 'image',
            'image_url': 'https://127.0.0.1:8000',
        }
        response = self.client.post('/api/image/create', data=self.data)
        self.assertEqual(response.json(), self.data)
        image = Image.objects.get(description=self.data['description'])
        self.data['id'] = image.id

        response = self.client.get(f"/api/image/{image.id}")
        self.assertEqual(response.json(), self.data)

    def test_image_detail_invalid(self):
        response = self.client.get("/api/image/fsd;lkas")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# bookmark
class BookmarkTestCase(SetUp, APITestCase):
    def test_bookmark(self):
        self.data = {
            'description': 'image',
            'image_url': 'https://127.0.0.1:8000',
        }
        self.client.post('/api/image/create', data=self.data)

        response = self.client.post(reverse('image_add_to_bookmark_url'), {'id': 1})
        self.assertEqual(response.json(), {'description': 'image', 'image_url': 'https://127.0.0.1:8000', 'id': 1})

        bookmark_detail_data = [{'description': 'image', 'id': 1, 'image_url': 'https://127.0.0.1:8000'}]
        response = self.client.get(reverse('bookmark_url'))
        self.assertEqual(response.json(), bookmark_detail_data)

class AddToBookmarkInvalidTestCase(SetUp, APITestCase):
    def test_add_to_bookmark(self):
        self.data = {'detail': 'The image has not found'}
        response = self.client.post(reverse('image_add_to_bookmark_url'), {'id': 1})
        self.assertEqual(response.json(), self.data)

class BookmarkDetailInvalidTestCase(APITestCase):
    def test_bookmark_detail_invalid(self):
        response = self.client.get(reverse('bookmark_url'))
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})


# tokens
class AccessTokenTestCase(APITestCase):
    def test_access_token(self):
        self.register_url = reverse("user_create_url")
        self.user_data = {
            "username": "test_user",
            "password": "123456789"
        }
        self.client.post(self.register_url,self.user_data)

        auth_url = reverse("token_obtain_pair_url")
        response = self.client.post(auth_url,{
            "username" : self.user_data.get("username") ,
            "password" : self.user_data.get("password")
        })

        if response.data.get('access'):
            return True
        else:
            return False

    def test_access_token_invalid(self):
        auth_url = reverse("token_obtain_pair_url")
        response = self.client.post(auth_url,{
            "username" : "ffds;" ,
            "password" : ";fsjdffsdafd"
        })
        self.assertEqual(response.json(), {'detail': 'No active account found with the given credentials'})


class RefreshTokenTestCase(SetUp, APITestCase):
    def test_refresh_token(self):
        self.data = {
            'refresh': self.refresh_token
        }

        response = self.client.post('/api/token/refresh', data={'refresh': self.refresh_token})
        if response.json()['access'] and response.json()['refresh']:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            print(False)

    def test_refresh_token_invalid(self):
        self.client.post('/api/token/refresh', data={'refresh': self.refresh_token})
        response = self.client.post('/api/token/refresh', data={'refresh': self.refresh_token})

        self.assertEqual(response.json(), {'detail': 'Token is blacklisted', 'code': 'token_not_valid'})


# profile
class RegistrationTestCase(APITestCase):
    def test_registration(self):
        self.register_url = reverse("user_create_url")
        self.user_data = {
            "username": "test_user1",
            "password": "123456789"
        }
        self.client.credentials(HTTP_AUTHORIZATION='fas;df')
        response = self.client.post(self.register_url, self.user_data)

        self.assertEqual(response.json(), {'username': 'test_user1'})

class ProfileTestCase(SetUp, APITestCase):
    def test_upload_image_profile(self):
        self.data = {
            'description': 'image',
            'image_url': 'https://127.0.0.1:8000',
        }

        response = self.client.post('/api/image/create', data=self.data)
        self.assertEqual(response.json(), self.data)

        image = Image.objects.get(image_url=self.data.get('image_url'))

        user = User.objects.get(username="test_user")

        self.data = {'username': 'test_user', 'email': '', 'is_staff': False, 'id': user.id, 'uploaded_photos': [image.id]}

        response = self.client.get('/api/profile')
        self.assertEqual(response.json(), self.data)

class ProfileInvalidTestCase(APITestCase):
    def test_profile_invalid(self):
        response = self.client.get('/api/profile')

        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})


# errors
class NotFoundTestCase(APITestCase):
    def test_not_found(self):
        response = self.client.get('/api/fsdjfkasj')
        self.assertEqual(response.json(), {'detail': 'Not found'})
