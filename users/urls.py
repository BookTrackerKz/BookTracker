from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/admin/", views.SuperUserView.as_view()),
    path("users/<str:pk>/", views.UserDetailView.as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view()),
    path("users/admin/create/", views.FirstAdminSuperUserView.as_view()),
]
