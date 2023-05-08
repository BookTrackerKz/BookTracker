from django.db import models
import uuid
from users.models import User


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=127)
    author = models.CharField(max_length=127)
    description = models.TextField(blank=True, null=True)
    publish_date = models.CharField(max_length=10)
    number_pages = models.IntegerField()
    language = models.CharField(max_length=20)
    isbn = models.CharField(max_length=13)

    category = models.ForeignKey(
        "categories.Category", on_delete=models.CASCADE, related_name="books"
    )
    publisher = models.ForeignKey(
        "publishing_company.Publisher",
        on_delete=models.CASCADE,
        related_name="book_published",
    )
    followers = models.ManyToManyField(
        User,
        through="books.BookFollowers",
        related_name="user_following_books",
    )

    class Meta:
        ordering = ["id"]


class BookFollowers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    followed_at = models.DateTimeField(auto_now_add=True)

    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="book_follower"
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_follower_book"
    )
