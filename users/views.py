from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.serializers import UserSerializer, UserUpdateSerializer, UserAdminSerializer
from users.permissions import OnlyUserCompanyCanAcces, IsStudentOwner, IsAllowed
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    CreateAPIView,
)


class UserView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAllowed]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class SuperUserView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class FirstAdminSuperUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudentOwner]

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
