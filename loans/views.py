from django.shortcuts import get_object_or_404
from rest_framework.views import Response, status
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    ListAPIView,
)
from datetime import date
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User, Loan
from copies.models import Copy
from loans.serializers import LoanSerializer
from loans.permissions import IsStaffUser, IsLoanOwner


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
            return Response(
                {"error": "This book copy is not available."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj = get_object_or_404(User, id=self.kwargs.get("user_id"))
        if user_obj.number_loans == 5:
            return Response(
                {
                    "error": "You have already reached the maximun number of loans. Please, return one book to be able to loan a new book"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_obj.cleared_date > date.today():
            return Response(
                {
                    "error": f"Your account is blocked to new loans until {user_obj.cleared_date}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class LoanDetailView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    lookup_url_kwarg = "loan_id"

    # def patch(self, request, *args, **kwargs):
    #     loan_data = get_object_or_404(Loan, id=self.kwargs.get("loan_id"))
    #     import ipdb

    #     ipdb.set_trace()
    #     return self.partial_update(loan_data, *args, **kwargs)


class UserLoanDetailView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffUser, IsLoanOwner]

    # queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        return Loan.objects.filter(user_id=self.kwargs.get("user_id"))
