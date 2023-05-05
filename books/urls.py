from django.urls import path
from . import views
from loans.views import LoanView
from copies.views import CopyDetailView
from copies.views import CopyDetailView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<str:book_id>/followers", views.BookFollowersView.as_view()),
    path("books/<uuid:id>/", views.BookDetailView.as_view()),
    path("books/<uuid:id>/copies/", CopyDetailView.as_view()),
    path("books/<uuid:copy_id>/loans/<uuid:user_id>/", LoanView.as_view()),
]
