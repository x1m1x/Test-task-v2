from django.db import models

class Image(models.Model):
    description = models.CharField(max_length=100)
    image_url = models.CharField(max_length=300)

    def __str__(self):
        return self.description
