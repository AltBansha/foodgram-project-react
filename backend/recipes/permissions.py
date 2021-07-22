from rest_framework import permissions

from users.models import UserRole


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Права доступа для автора"""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminOrSuperUser(permissions.BasePermission):
    """Права доступа для администратора"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or (request.user.is_staff
                    or request.user.role == UserRole.ADMIN))
