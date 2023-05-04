from rest_framework import serializers
from .models import Copy
from django.utils import timezone
import uuid


class CopySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    partial = True

    def update(self, instance, validated_data):
        instance.is_availabe = validated_data.get("is_available", instance.is_available)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return super().update(instance, validated_data)

    class Meta:
        model = Copy

        fields = [
            "id",
            "is_available",
            "classification_code",
            "book_id",
            "is_active",
            "deleted_at",
        ]
