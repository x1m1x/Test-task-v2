import jwt

from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    description = models.CharField(max_length=100)
    image_url = models.CharField(max_length=300, unique=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="uploaded_by")
    bookmark = models.ForeignKey("Bookmark", on_delete=models.SET_NULL, null=True, blank=True, related_name="bookmark")
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.description

class Bookmark(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
