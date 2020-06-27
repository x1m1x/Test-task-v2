from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    description = models.CharField(max_length=100)
    image_url = models.CharField(max_length=300)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="uploaded_by")
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="liked_by")
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.description
