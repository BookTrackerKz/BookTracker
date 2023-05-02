from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> User:
        if validated_data["is_superuser"]:
            return User.objects.create_superuser(**validated_data)

        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "is_superuser",
            "id", "password",
            "cpf",
            "is_staff",
            "number_loans"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "cpf": {"write_only": True}
        }
        # depth = 1
