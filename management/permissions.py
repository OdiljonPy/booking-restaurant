from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.status == 3:
            return True
        return False

    def has_permission(self, request, view):
        if request.user.status == 3:
            return True
        return False


class IsAdministrator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.status == 4:
            return True
        return False

    def has_permission(self, request, view):

        if request.user.status == 4:
            return True
        return False
