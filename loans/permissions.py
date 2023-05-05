from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User


class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:

        # if request.method in permissions.SAFE_METHODS
        # if request.user.is_authenticated:
        #     return request.user.is_staff 
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated and request.user.is_staff 
    
class IsLoanOwner(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, obj: User
    ) -> bool:
        return obj.user == request.user

# def has_object_permission(self, request, view: View, obj: User) -> bool:        
#         return request.user.is_authenticated and obj == request.user or request.user.is_staff
