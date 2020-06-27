from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Image


# Images

class ImageSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    image_url = serializers.URLField(max_length=300)
    id = serializers.IntegerField()

    class Meta:
        fields = ('description', 'image_url', 'id')

class ImageCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    image_url = serializers.URLField()

    class Meta:
        model = Image
        fields = ('description', 'image_url', 'id')

class ImageAddToBookmarkSerializer(serializers.Serializer):
    add_to_bookmark = serializers.BooleanField()

    class Meta:
        fields = ('add_to_bookmark', )


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'description', 'image_url',)
# Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserCreateSerializer, self).create(validated_data)
