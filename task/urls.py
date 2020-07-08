from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    # images
    path('', ImageList.as_view(), name="images_list_url"),
    path('image/create/', ImageCreate.as_view(), name="image_create_url"),
    path('image/<int:id>/', ImageDetail.as_view(), name="image_detail_url"),
    # bookmark
    path('image/add_to_bookmark/', ImageAddToBookmark.as_view(), name="image_add_to_bookmark_url"),
    path('bookmark/', BookmarkDetail.as_view(), name="bookmark_url"),
    # users
    path('register/', RegistrationAPIView.as_view(), name="user_create_url"),
    path('profile/', UserProfile.as_view(), name="user_profile_url"),
    # token
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair_url"),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name="token_refresh_url"),

    path('image/create', ImageCreate.as_view(), name="image_create_url"),
    path('image/<int:id>', ImageDetail.as_view(), name="image_detail_url"),
    # bookmark
    path('image/add_to_bookmark', ImageAddToBookmark.as_view(), name="image_add_to_bookmark_url"),
    path('bookmark', BookmarkDetail.as_view(), name="bookmark_url"),
    # users
    path('register', RegistrationAPIView.as_view(), name="user_create_url"),
    path('profile', UserProfile.as_view(), name="user_profile_url"),
    # token
    path('token', TokenObtainPairView.as_view(), name="token_obtain_pair_url"),
    path('token/refresh', CustomTokenRefreshView.as_view(), name="token_refresh_url"),
]
