from rest_framework import permissions
from .models import Manager, Administrator


class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.status == 3 and Manager.objects.filter(user_id=request.user.id,
                                                                   restaurant_id=obj.id).exists()


class IsManagerOrAdministrator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.status == 3:
            return Manager.objects.filter(user_id=request.user.id, restaurant_id=obj.id).exists()
        if request.user.status == 4:
            return Administrator.objects.filter(user_id=request.user.id, manager__restaurant_id=obj.id).exists()

        return False
