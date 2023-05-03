from django.db import models
import uuid


class Copy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_available = models.BooleanField()
    classification_code = models.CharField(max_length=13)

    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="copies"
    )
