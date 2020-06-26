from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from pexels_api import API

from django.contrib.auth.models import User

from .models import Image
from .serializers import ImageSerializer, ImageCreateSerializer, UserSerializer

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

    for image_obj in Image.objects.all():
        dict = {
        'description': image_obj.description,
        'image_url': image_obj.image_url,
        'id': image_obj.id
        }
        images.append(dict)

    return images

class ImageList(APIView):
    serializer_class = ImageSerializer

    def get(self, request):
        if request.GET.get('search'):
            return Response(get_images(request.GET.get('search')))
        return Response(get_images())

class ImageCreate(generics.CreateAPIView):
    serializer_class = ImageCreateSerializer

class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    def get(self, request, id):
        try:
            User.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.user.id == id:
            user = User.objects.get(id=id)
            properties = {
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'id': user.id
            }
            return Response(properties)
        else:
            print(request.user.id)
            return Response(status=status.HTTP_403_FORBIDDEN)
