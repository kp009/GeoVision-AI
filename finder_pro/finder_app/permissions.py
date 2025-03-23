from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    """Allows access only to superadmins."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'superadmin'

class IsAdminOrSuperAdmin(BasePermission):
    """Allows access to admins and superadmins."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'superadmin']

class IsUser(BasePermission):
    """Allows access only to regular users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'
