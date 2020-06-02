from rest_framework import permissions

from .models import Post


class PostPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        posted = Post.objects.filter(author=user).exists()
        return posted