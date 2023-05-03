
from django import views
from django.urls import path
from loans.views import LoanDetailView

urlpatterns = [
    path("loans/<uuid:loan_id>/", views.LoanDetailView.as_view())
]

