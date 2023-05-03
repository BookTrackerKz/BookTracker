from rest_framework import permissions
from rest_framework.views import Request, View


class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:

        if request.user.is_authenticated:
            return request.user.is_staff 
        return False
