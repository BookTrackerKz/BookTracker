from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    # email = serializers.CharField (
    #     validators= [
    #         UniqueValidator(
    #             queryset=User.objects.all(),
    #             message="user with this email already exists.",
    #         )
    #     ]
    # ),
    # username = serializers.CharField (        
    #     validators= [
    #         UniqueValidator(
    #             queryset=User.objects.all(),
    #             message="A user with that username already exists.",
    #         )
    #     ],
    # ),
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
        # depth = 1
    
    # def update(self, instance: User, validated_data: dict) -> User:
    #     for key, value in validated_data.items():
    #         if key == "password":
    #             instance.set_password(value)
    #         else:
    #             setattr(instance, key, value)

    #     instance.save()

    #     return instance
