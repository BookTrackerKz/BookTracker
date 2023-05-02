from django.db import models
import uuid


class Book(models.Model):
    class Meta:
        ordering = ["id"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=127)
    author= models.CharField(max_length=127)
    description=models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        "categories.Category", on_delete=models.CASCADE, related_name="books"
    )
    publish_date = models.CharField(max_lenght=10)
    number_pages = models.IntegerField()
    language= models.CharField(max_legth=20)
    publisher=models.ForeignKey(
        "publishing_company.Publisher", on_delete=models.CASCADE, related_name="books"
    )
    isbn=models.CharField(max_length=13)
    followers=models.ManyToManyField(
        "users.User",
        related_name="following_books",
    )
