from django.urls import path
from loans.views import (
    LoanNotificationCloseToDueDate,
    LoanNotificationDelayedView,
    LoanDetailView,
    UserLoanDetailView,
)

urlpatterns = [
    path("loans/duedates/", LoanNotificationCloseToDueDate.as_view()),
    path("loans/delays/", LoanNotificationDelayedView.as_view()),
    path("loans/<loan_id>/", LoanDetailView.as_view()),
    path("loans/<user_id>/users/", UserLoanDetailView.as_view()),
]
