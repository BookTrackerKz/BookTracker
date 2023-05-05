from django import views
from django.urls import path
from loans.views import LoanDetailView, UserLoanDetailView

urlpatterns = [
    path("loans/<loan_id>/", LoanDetailView.as_view()),
    path("loans/<user_id>/users/", UserLoanDetailView.as_view()),
]
