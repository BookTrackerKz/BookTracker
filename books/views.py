from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from .permissions import CustomBookPermissions
from copies.models import Copy
from .models import Book
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


class BookDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermissions]
    queryset = Book.objects.all()
    serializer_class = BookSerializerUpdate
    lookup_field = "id"
