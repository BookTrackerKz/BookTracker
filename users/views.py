from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from .models import User
# from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
# from .permissions import IsAccountOwner
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView


# Create your views here.

class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
