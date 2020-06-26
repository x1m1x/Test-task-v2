from django.urls import path

from .views import *


urlpatterns = [
    path('', ImageList.as_view(), name="images_list_url"),
    path('image/create/', ImageCreate.as_view(), name="image_create_url"),
    path('profile/<int:id>/', UserProfile.as_view(), name="user_profile_url"),
]
