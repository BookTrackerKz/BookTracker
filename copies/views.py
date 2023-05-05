from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import Response
from .serializers import CopySerializer
from books.permissions import CustomBookPermissions
from .models import Copy
from django.utils import timezone


class CopyDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomBookPermissions]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer
    lookup_url_kwarg = "copy_id"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_available = False
        instance.is_active = False
        instance.deleted_at = timezone.now()
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
