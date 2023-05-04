from rest_framework import permissions
from .models import User
from rest_framework.views import View

    
class IsAllowedUserToRetrieveAndModify(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            else:
                if request.method in permissions.SAFE_METHODS:
                    return True
        return False

class IsEstudentOwner(permissions.BasePermission):   

    def has_object_permission(self, request, view: View, obj: User) -> bool:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.method in permissions.SAFE_METHODS or request.method == "PATCH":
                if request.user.is_staff or request.method == "DELETE":
                        return True
                if obj.id == request.user.id:
                    return True
