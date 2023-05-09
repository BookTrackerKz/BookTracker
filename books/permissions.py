from rest_framework import permissions
from rest_framework.views import View, Request
from users.models import User


class CustomBookPermissions(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff


class IsStudentAccount(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        if request.user.is_authenticated:
            if obj.id == request.user.id:
                return True
