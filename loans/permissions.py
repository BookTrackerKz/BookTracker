from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User


class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated and request.user.is_staff


class IsLoanOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.user.is_authenticated:
            if str(view.kwargs.get("user_id")) == str(request.user.id):
                return True
            if request.user.is_staff:
                return True
        return False
