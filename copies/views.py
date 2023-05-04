from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CopySerializer
from books.permissions import CustomBookPermissions
from .models import Copy


# Create your views here.
class CopyDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermissions]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer
    lookup_field = "id"
