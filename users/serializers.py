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

    def update(self, instance: User, validated_data: dict) -> User:
        user_auth = self.context["request"].user
        if not user_auth.is_superuser:
            if validated_data.get("is_superuser"):
                validated_data.pop("is_superuser")
            if validated_data.get("is_staff"):
                validated_data.pop("is_staff")
            if validated_data.get("is_active"):
                validated_data.pop("is_active")

        User.objects.update(**validated_data)

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


class UserUpdateSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["cleared_date", "is_superuser", "is_staff", "is_active"]
        extra_kwargs = {
            "password": {"write_only": True},
            "cpf": {
                "write_only": True,
            },
        }


class UserAdminSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> User:
        validated_data["cleared_date"] = date.today()
        return User.objects.create_superuser(**validated_data)

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


class UserUpdateSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["cleared_date", "is_superuser", "is_staff", "is_active"]
        extra_kwargs = {
            "password": {"write_only": True},
            "cpf": {
                "write_only": True,
            },
        }
