from rest_framework import permissions
from .models import User
from rest_framework.views import View


class OnlyUserCompanyCanAcces(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            else:
                if request.method in permissions.SAFE_METHODS and request.user.is_staff:
                    return True
        return False


class IsStudentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if (
                request.method in permissions.SAFE_METHODS
                and request.user.is_staff
                or request.user.is_staff
                and not obj.is_superuser
                and not obj.is_staff
                and request.method == "PATCH"
            ):
                return True
            if obj.id == request.user.id and request.method != "DELETE":
                return True
            if (
                request.user.is_staff
                and not obj.is_superuser
                and not obj.is_staff
                and request.method == "DELETE"
            ):
                return True


class IsAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        if request.user.is_authenticated:
            if request.user.is_staff and request.method == "GET":
                return True
        return False
