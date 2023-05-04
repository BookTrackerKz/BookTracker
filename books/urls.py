from django.urls import path
from . import views
from copies.views import CopyDetailView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<uuid:id>/", views.BookDetailView.as_view()),
    path("books/<uuid:id>/copies/", CopyDetailView.as_view()),
]
