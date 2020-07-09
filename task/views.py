from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenRefreshView

from pexels_api import API

from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Image, Bookmark
from .serializers import *


def get_images(query=None, limit=None):
    api_key = '563492ad6f917000010000010ff082d5518a4fbd9b0710fafd7c9769'
    api = API(api_key)

    limited_images = []

    if query and not limit:
        api.search(query=query, page=1, results_per_page=100)

    elif limit and not query:
        try:
            limit = int(limit)
        except:
            return {'detail': 'Bad request'}

        if limit >= 300:
            return {'detail': 'Bad request'}
        else:
            if limit >= 80:
                max_page = int(limit/80)
                for i in range(1, max_page+1):
                    api.popular(page=i, results_per_page=80)
                    limited_images.append(api.get_entries())
            else:
                api.popular(page=1, results_per_page=limit)
                limited_images.append(api.get_entries())

    elif limit and query:
        try:
            limit = int(limit)
        except:
            return {'detail': 'Bad request'}

        if limit >= 300:
            return {'detail': 'Bad request'}
        else:
            if limit >= 80:
                max_page = int(limit/80)
                for i in range(1, max_page+1):
                    api.search(query=query, page=i, results_per_page=80)
                    limited_images.append(api.get_entries())
            else:
                api.search(query=query, page=1, results_per_page=limit)
                limited_images.append(api.get_entries())
    else:
        api.popular(page=1, results_per_page=100)

    if api.get_entries():
        all_images = api.get_entries()
    else:
        all_images = []

    for image_obj in Image.objects.filter(show=True):
        if limited_images:
            if len(all_images) >= int(limit):
                break
            all_images.append(image_obj)
        all_images.append(image_obj)


    if limited_images:
        for i in limited_images:
            for j in i:
                if len(all_images) >= int(limit):
                    break
                all_images.append(j)

    images_json = []
    for i in all_images:
        try:
            dict = {
                'description': i.description,
                'image_url': i.original,
                'id': i.id
            }
        except:
            dict = {
                'description': i.description,
                'image_url': i.image_url,
                'id': i.id
            }

        images_json.append(dict)

    return images_json


# Images
class ImageList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer


    def get(self, request):
        search = request.GET.get('search')
        limit = request.GET.get('limit')

        if search and not limit:
            return Response(get_images(search) )
        elif limit and not search:
            return Response(get_images(limit=limit) )
        elif search and limit:
            return Response(get_images(limit=limit, query=search) )
        return Response(get_images())

class ImageDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer
    lookup_field = "id"

    def get_image(self, id):
        for image in get_images():
            if image['id'] == id:
                return image
            else:
                continue

    def get(self, request, id):
        image = self.get_image(int(id))
        if image:
            return Response(image)
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

class ImageCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageCreateSerializer
    def post(self, request):
        serializer = ImageCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(uploaded_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"image_url": ["Such image is already exist"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# bookmark
class ImageAddToBookmark(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageAddToBookmarkSerializer
    def get_image(self, id):

        for image in get_images():
            if image['id'] == id:
                return image
            else:
                continue

    def post(self, request):
        id = request.data['id']
        image_json = self.get_image(int(id))
        if image_json == None:
            return Response({'detail': 'The image has not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            image = Image.objects.get(id=id)
            image.bookmark = Bookmark.objects.get(user=request.user.id)
            image.save()
        except Image.DoesNotExist:
            image = Image.objects.create(description=image_json['description'],
                                         id=image_json['id'],
                                         image_url=image_json['image_url'],
                                         show=False,
                                         bookmark=Bookmark.objects.get(user=request.user.id))
            image.save()
        except Bookmark.DoesNotExist:
            Bookmark.objects.create(user=request.user).save()
            
        return Response(image_json, status=status.HTTP_201_CREATED)

class BookmarkDetail(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer
    def get(self, request):
        images_json = []
        try:
            bookmark = Bookmark.objects.get(user=request.user)
        except:
            return Response({'detail': 'Please sign in'}, status=status.HTTP_401_UNAUTHORIZED)
        for i in bookmark.bookmark.all():
            images_json.append(
                {
                    'description': i.description,
                    'id': i.id,
                    'image_url': i.image_url
                }
            )
        return Response(images_json)


# Users
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        uploaded_images = []
        for image in Image.objects.filter(uploaded_by=request.user):
            uploaded_images.append(image.id)

        json = {
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'id': user.id,
            'uploaded_photos': uploaded_images
        }
        return Response(json)

    def put(self, request):
        user = User.objects.get(id=request.user.id)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = User.objects.get(id=request.user.id)
        user.delete()
        return Response({"detail": "Successfully deleted!"})

# class UserCreate(generics.CreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = UserCreateSerializer
#     queryset = User.objects.all()
#     def post(self, request):
#         serializer = UserCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             Bookmark.objects.create(user=User.objects.get(username=request.data['username'])).save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Bookmark.objects.create(user=User.objects.get(username=serializer.data['username'])).save()

        return Response(
            {
                "username": serializer.data['username'],
            },
            status=status.HTTP_201_CREATED,
        )

# Tokens
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomRefreshTokenSerializer
