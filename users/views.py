from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.serializers import UserSerializer
from users.permissions import IsAllowedUserToRetrieveAndModify
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView


class UserView(ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class SuperUserView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAllowedUserToRetrieveAndModify]

    queryset = User.objects.all()
    serializer_class = UserSerializer