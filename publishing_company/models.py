from django.db import models
import uuid


class Publisher(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=127)
