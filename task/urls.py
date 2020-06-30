from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *


urlpatterns = [
    path('', ImageList.as_view(), name="images_list_url"),
    path('image/create/', ImageCreate.as_view(), name="image_create_url"),
    path('image/<int:id>/add_to_bookmark/', ImageAddToBookmark.as_view(), name="image_add_to_bookmark_url"),
    path('bookmark/', Bookmark.as_view(), name="bookmark_url"),
    # users
    path('register/', UserCreate.as_view(), name="user_create_url"),
    path('profile/', UserProfile.as_view(), name="user_profile_url"),
    # token
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
