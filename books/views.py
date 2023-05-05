from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import Response, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .permissions import CustomBookPermissions
from users.permissions import IsAllowedUserToRetrieveAndModify
from .models import Book, BookFollowers
from users.models import User
from .serializer import BookSerializer, BookFollowersSerializer, BookSerializerUpdate


class BookView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermissions]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        route_parameter = self.request.query_params.get("category")  # (1)

        if route_parameter:
            queryset = Book.objects.filter(category__name__icontains=route_parameter)
            return queryset

        return super().get_queryset()


class BookDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermissions]
    queryset = Book.objects.all()
    serializer_class = BookSerializerUpdate
    lookup_field = "id"


class BookFollowersView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BookFollowers.objects.all()
    serializer_class = BookFollowersSerializer

    def create(self, request, *args, **kwargs):
        book_data = get_object_or_404(Book, id=self.kwargs.get("book_id"))
        user_data = get_object_or_404(User, id=self.request.user.id)
        followed = BookFollowers.objects.filter(
            book_id=book_data.id, user_id=user_data.id
        ).first()
        if followed:
            return Response(
                {"error": "You have already followed this book"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer) -> None:
        book_data = get_object_or_404(Book, id=self.kwargs.get("book_id"))
        user_data = get_object_or_404(User, id=self.request.user.id)

        serializer.save(book=book_data, user=user_data)


class BookFollowersDetailView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAllowedUserToRetrieveAndModify]
    queryset = BookFollowers.objects.all()
    serializer_class = BookFollowersSerializer
    lookup_field = "id"
