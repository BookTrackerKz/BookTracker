from datetime import date
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> User:
        user_auth = self.context["request"].user
        validated_data["cleared_date"] = date.today()
        if user_auth.is_superuser:
            if validated_data.get("is_superuser"):
                return User.objects.create_superuser(**validated_data)

            return User.objects.create_user(**validated_data)

        staff = validated_data.pop("is_staff", False)
        superuser = validated_data.pop("is_superuser", False)

        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "is_superuser",
            "id",
            "password",
            "cpf",
            "is_staff",
            "number_loans",
            "cleared_date",
        ]
        read_only_fields = ["cleared_date"]
        extra_kwargs = {
            "password": {"write_only": True},
            "cpf": {
                "write_only": True,
            },
        }
