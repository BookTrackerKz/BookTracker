from django.shortcuts import get_object_or_404
from rest_framework.views import Response, status
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    ListAPIView,
    ListCreateAPIView,
)
import datetime
import time
from datetime import date, timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User, Loan
from copies.models import Copy
from loans.serializers import LoanSerializer
from loans.permissions import IsStaffUser, IsLoanOwner
from django.conf import settings
from django.core.mail import send_mail


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
        if user_obj.number_loans == settings.MAX_LOANS:
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


class LoanNotificationDelayedView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffUser]

    print("*" * 10)
    # queryset = Loan.objects.all()
    # serializer_class = LoanSerializer
    # print("*" * 10)

    def get_queryset(self):
        user_emails = []

        today = date.today()
        print(type(Loan.loan_estimate_return))

        return_date = time.mktime(
            datetime.datetime.strptime(Loan.loan_estimate_return, format="%Y-%m-%d")
        )

        loans = Loan.objects.filter(return_date < today)

        if loans.__len__ > 0:
            for loan in loans:
                user_email = [loan.user.email]
                book = loan.copy
                import ipdb

                ipdb.set_trace()
                send_mail(
                    subject="Livro solicitado esta disponível",
                    message=f"O livro {loan.copy.book.title} encontra-se atrasado para devolucao. Por favor, compareça à biblioteca para devolvê-lo",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=user_email,
                    fail_silently=False,
                )
        return Loan.objects.all()


class LoanNotificationCloseToDueDate(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffUser]

    print("*" * 10)
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    # user_emails = []
    # tomorrow = date.today() + timedelta(1)
    # loans = Loan.objects.filter(Loan.loan_estimate_return == tomorrow)

    # if user_emails:
    #     for loan in loans:
    #         user_email = [loan.user.email]
    #         book = loan.copy
    #         import ipdb

    #         ipdb.set_trace()
    #         send_mail(
    #             subject="Livro solicitado esta disponível",
    #             message=f"O livro {loan.copy.book.title} encontra-se atrasado para devolucao. Por favor, compareça à biblioteca para devolvê-lo",
    #             from_email=settings.EMAIL_HOST_USER,
    #             recipient_list=user_emails,
    #             fail_silently=False,
    #         )
