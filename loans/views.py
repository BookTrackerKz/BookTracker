from django.shortcuts import get_object_or_404
from rest_framework.views import Response,  status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from loans.models import Loan
from users.models import User
from copies.models import Copy
from loans.serializers import LoanSerializer
from loans.permissions import IsStaffUser


class LoanView(CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


    def perform_create(self, serializer) -> None:
        user_data = get_object_or_404(User, id=self.kwargs.get("user_id"))
        copy_data = get_object_or_404(Copy, id=self.kwargs.get("copy_id"))
        serializer.save(user=user_data, copy=copy_data)

    def create(self, request, *args, **kwargs):
        copy_data = get_object_or_404(Copy, id=self.kwargs.get("copy_id"))
        if not copy_data.is_available:
            return Response({"error": "This book copy is not available."}, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




class LoanDetailView(UpdateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer