from rest_framework import serializers
from .models import Copy
import uuid


class CopySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, read_only=True
    )

    class Meta:
        model = Copy
        fields = ["is_available", "classification_code", "book_id", "is_active", "deleted_at"]
