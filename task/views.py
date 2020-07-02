from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from pexels_api import API

from django.db import IntegrityError
from django.shortcuts import render

from django.http import HttpResponseNotFound

from django.contrib.auth.models import User

from .models import Image
from .serializers import *
from .permissions import IsNotAuthenticatedOrReadOnly

import json


def error500(request):
    response_data = {}
    response_data['detail'] = 'Server error'
    return HttpResponseNotFound(json.dumps(response_data), content_type="application/json", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def error404(request, exception):
    response_data = {}
    response_data['detail'] = 'Not found.'
    return HttpResponseNotFound(json.dumps(response_data), content_type="application/json")

def get_images(query=None):
    api_key = '563492ad6f917000010000010ff082d5518a4fbd9b0710fafd7c9769'
    api = API(api_key)
    if query != None:
        api.search(query=query, page=1, results_per_page=100)
    else:
        api.popular(page=1, results_per_page=100)

        all_images = api.get_entries()

    images = []
    for i in all_images:
        dict = {
        'description': i.description,
        'image_url': i.original,
        'id': i.id
        }
        images.append(dict)

    for image_obj in Image.objects.filter(show=True):
        dict = {
        'description': image_obj.description,
        'image_url': image_obj.image_url,
        'id': image_obj.id
        }
        images.append(dict)

    return images

# Images

class ImageList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer


    def get(self, request):
        if request.GET.get('search'):
            return Response(get_images(request.GET.get('search')))
        return Response(get_images())

class ImageCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageCreateSerializer
    def get_image(self, id):
        for image in get_images():
            if image['id'] == id:
                return image
            else:
                continue
    def post(self, request):
        serializer = ImageCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(uploaded_by=request.user)
            except IntegrityError:
                return Response({"id": ["Such image is already exist"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ImageAddToBookmark(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageAddToBookmarkSerializer
    def get_image(self, id):
        for image in get_images():
            if image['id'] == id:
                return image
            else:
                continue

    def get(self, request, id):
        image_json = self.get_image(id)
        if image_json == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            image = Image.objects.get(id=id)
        except Image.DoesNotExist:
            image = Image.objects.create(description=image_json['description'],
                                         id=image_json['id'],
                                         image_url=image_json['image_url'],
                                         show=False,
                                         liked_by=request.user)
            image.save()
        return Response(image_json, status=status.HTTP_201_CREATED)

class Bookmark(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    def get_queryset(self):
        return Image.objects.filter(liked_by=self.request.user)

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


class UserCreate(generics.CreateAPIView):
    permission_classes = [IsNotAuthenticatedOrReadOnly]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
