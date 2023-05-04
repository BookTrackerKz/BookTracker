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
                    if request.user.is_staff:
                        return True
                    else:
                        return False

    def has_object_permission(self, request, view: View, obj: User) -> bool:        
        return request.user.is_authenticated and obj == request.user or request.user.is_staff
    
    

         


            

