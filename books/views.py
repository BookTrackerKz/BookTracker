from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import CustomBookPermissions
from .models import Book
from .serializer import BookSerializer


class BookView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermissions]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
