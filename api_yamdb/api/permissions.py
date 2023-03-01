from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_staff
            or (
                request.user.is_authenticated
                and request.user.is_admin)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin)
        )


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user
                    and (request.user.role == 'admin'
                         or request.user.is_staff)
                    )
