from rest_framework import serializers
from datetime import date
from users.models import User, Loan
from copies.models import Copy
from django.shortcuts import get_object_or_404
import uuid


class LoanSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> Loan:

        copy_obj = get_object_or_404(Copy, pk=validated_data["copy_id"])
        copy_obj.is_available = True
        copy_obj.save()

        user_obj = get_object_or_404(User, id=self.kwargs.get("user_id"))
        user_obj.number_loans += 1
        user_obj.save()

        return Loan.objects.create(**validated_data)

    def update(self, instance:Loan, validated_data:dict) -> Loan:
        copy_obj = get_object_or_404(Copy, pk=instance.copy_id)
        copy_obj.is_available = True
        copy_obj.save()

        user_obj = get_object_or_404(User, pk=instance.user_id)
        user_obj.number_loans -= 1
        user_obj.save()

        instance.loan_return = date.today()
        instance.save()
        return instance

    id = serializers.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, read_only=True
    )
    loan_withdraw = serializers.DateField(read_only=True)

    class Meta:
        model = Loan
        fields = ["copy_id", "user_id", "loan_return"]

    
