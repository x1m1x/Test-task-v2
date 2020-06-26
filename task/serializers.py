from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Image

class ImageSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    image_url = serializers.URLField(max_length=300)
    id = serializers.IntegerField()

    class Meta:
        fields = ('description', 'image_url', 'id')

class ImageCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Image
        fields = ('description', 'image_url', 'id')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff', 'id')
