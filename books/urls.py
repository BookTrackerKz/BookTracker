from django.urls import path
from . import views
from loans.views import LoanView
from copies.views import CopyDetailView
from copies.views import CopyDetailView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/followers/", views.BookFollowersView.as_view()),
    path("books/<book_id>/followers/", views.BookFollowersView.as_view()),
    path("books/followers/<id>/", views.BookFollowersDetailView.as_view()),
    path("books/<id>/", views.BookDetailView.as_view()),
    path("books/<copy_id>/copies/", CopyDetailView.as_view()),
    path("books/<copy_id>/loans/<user_id>/", LoanView.as_view()),
]
