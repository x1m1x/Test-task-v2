from rest_framework import serializers

import jwt

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User

from .models import Image

import jwt

# Images

class ImageSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    image_url = serializers.URLField(max_length=300)
    id = serializers.IntegerField()

    class Meta:
        fields = ('description', 'image_url', 'id')

class ImageCreateSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField()

    class Meta:
        model = Image
        fields = ('description', 'image_url')

class ImageAddToBookmarkSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    class Meta:
        fields = ('id', )


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'description', 'image_url',)
# Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')

# Tokens

class CustomRefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh_token = RefreshToken(attrs['refresh'])
        refresh_token_bytes = bytes(str(refresh_token), 'utf-8')

        decoded_refresh_token = jwt.decode(refresh_token_bytes, None, None)

        refresh_token.blacklist()

        token = RefreshToken().for_user(User.objects.get(id=decoded_refresh_token['user_id']))
        return {'access': str(token.access_token),
                'refresh': str(token)}


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Creates a new user.
    Email, username, and password are required.
    Returns a JSON web token.
    """

    # The password must be validated and should not be read by the client
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
