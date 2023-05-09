from django.shortcuts import get_object_or_404
from rest_framework.views import Response, status, APIView
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    ListAPIView,
)
import datetime
import time
from datetime import date, timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User, Loan
from copies.models import Copy
from loans.serializers import LoanSerializer, LoanDelaySerializer
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


class UserLoanDetailView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLoanOwner]

    serializer_class = LoanSerializer

    def get_queryset(self):
        user_data = get_object_or_404(User, id=self.kwargs.get("user_id"))
        return Loan.objects.filter(user_id=self.kwargs.get("user_id"))


class LoanNotificationDelayedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffUser]

    def get(self, request, *args, **kwargs):
        delayed_loans_emails = []
        today = time.time()

        total_loans = Loan.objects.filter(loan_return=None)

        for loan in total_loans:
            estimate_return_date = time.mktime(
                datetime.datetime.strptime(
                    str(loan.loan_estimate_return), "%Y-%m-%d"
                ).timetuple()
            )

            if estimate_return_date < today:
                user_email = [loan.user.email]
                send_mail(
                    subject="Empréstimo atrasado.",
                    message=f"O livro {loan.copy.book.title} encontra-se atrasado para devolucao. Por favor, compareça à biblioteca para devolvê-lo.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=user_email,
                    fail_silently=False,
                )
                delayed_loans_emails.append(user_email)

        serializer = LoanDelaySerializer(delayed_loans_emails, many=True)

        return Response(serializer.data)


class LoanNotificationCloseToDueDate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffUser]

    def get(self, request, *args, **kwargs):
        loans_close_to_due_date_emails = []
        today = date.today()

        new_today = time.mktime(
            datetime.datetime.strptime(str(today), "%Y-%m-%d").timetuple()
        )

        tomorrow = new_today + 86400

        total_loans = Loan.objects.filter(loan_return=None)

        for loan in total_loans:
            estimate_return_date = time.mktime(
                datetime.datetime.strptime(
                    str(loan.loan_estimate_return), "%Y-%m-%d"
                ).timetuple()
            )

            if estimate_return_date == tomorrow:
                user_email = [loan.user.email]
                send_mail(
                    subject=f"Empréstimo próximo do",
                    message=f"O empréstimo do livro {loan.copy.book.title} se encerra em {today + timedelta(1)}. Por favor, compareça à biblioteca para devolvê-lo.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=user_email,
                    fail_silently=False,
                )
                loans_close_to_due_date_emails.append(user_email)

        serializer = LoanDelaySerializer(loans_close_to_due_date_emails, many=True)

        return Response(serializer.data)
