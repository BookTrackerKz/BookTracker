from datetime import date, timedelta
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
import holidays


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data: dict) -> User:

        user_auth = self.context["request"].user
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
            "number_loans"
        ]
        # read_only_fields = ["first_name", "last_name", "email"]
        extra_kwargs = {
            "password": {"write_only": True},
            "cpf": {"write_only": True,},
        }

    
    # def update(self, instance: User, validated_data: dict) -> User:
    #     for key, value in validated_data.items():
    #         if key == "password":
    #             instance.set_password(value)
    #         else:
    #             setattr(instance, key, value)

    #     instance.save()

    #     return instance
