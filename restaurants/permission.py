from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.author.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.author.id != request.author.id and not request.author.is_authenticated:
            if request.method in ['HEAD', 'GET', 'OPTIONS']:
                return True
            return False
        return True
