from django.shortcuts import get_object_or_404
from rest_framework.views import Request, Response, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import PageNumberPagination
from .permissions import CustomBookPermissions
from copies.models import Copy
from copies.models import Copy
from .models import Book
from .serializer import BookSerializer, BookFollowersSerializer
from .serializer import BookSerializer, BookSerializerUpdate


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


class BookFollowersView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookFollowersSerializer

    # def post(self, request: Request, book_id: int) -> Response:
    #     get_object_or_404(Book, pk=book_id)
    #     serializer = BookFollowersSerializer(data=request.data)

    #     serializer.is_valid(raise_exception=True)

    #     serializer.save(user=request.user.id, book=book_id)

    #     return Response(serializer.data, status.HTTP_201_CREATED)


class BookDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermissions]
    queryset = Book.objects.all()
    serializer_class = BookSerializerUpdate
    lookup_field = "id"
