from rest_framework import permissions


class IsNotAuthenticatedOrReadOnly(permissions.BasePermission):
    message = "You have already signed in"

    def has_permission(self, request, view):
        return not request.user.is_authenticated
