from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.status == 'is_admin':
            return True
        return False

    def has_permission(self, request, view):
        if request.user.status == 'is_admin':
            return True
        return False


class IsManagerOrIsAdministrator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow full access to admin users
        if request.user.status == 'is_admin':
            return True

        # Allow access to managers for objects related to their restaurant
        if hasattr(request.user, 'restaurant') and hasattr(obj, 'restaurant'):
            return obj.restaurant == request.user.restaurant

        # Deny access if neither admin nor manager for their restaurant
        return False

    def has_permission(self, request, view):
        # Allow full access to admin users
        if request.user.is_staff:
            return True

        # Allow access to managers for general actions related to their restaurant
        if hasattr(request.user, 'restaurant'):
            return True
        # Deny access if neither admin nor manager
        return False
