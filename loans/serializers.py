from rest_framework import serializers
from datetime import date, timedelta
from users.models import User, Loan
from users.serializers import UserSerializer
from copies.models import Copy
from copies.serializers import CopySerializer
from django.shortcuts import get_object_or_404
import holidays


class LoanSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> Loan:
        copy_obj = validated_data["copy"]
        copy_obj.is_available = False
        copy_obj.save()

        user_obj = validated_data["user"]
        user_obj.number_loans += 1
        user_obj.save()

        today_date = date.today()

        loan_delta = timedelta(14)
        br_holidays = holidays.BR()
        estimated_return = today_date + loan_delta

        week_day = estimated_return.weekday()
        if week_day == 4 and estimated_return in br_holidays:
            estimated_return += timedelta(3)
        elif week_day == 5:
            estimated_return += timedelta(2)
        elif week_day == 6:
            estimated_return += timedelta(1)

        if estimated_return in br_holidays:
            estimated_return += timedelta(1)

        validated_data["loan_estimate_return"] = estimated_return

        return Loan.objects.create(**validated_data)

    def update(self, instance: Loan, validated_data: dict) -> Loan:
        import ipdb

        copy_obj = get_object_or_404(Copy, pk=instance.copy_id)
        copy_obj.is_available = True
        copy_obj.save()

        user_obj = get_object_or_404(User, pk=instance.user_id)
        user_obj.number_loans -= 1
        if instance.loan_estimate_return < date.today():
            user_obj.cleared_date = date.today() + timedelta(7)
        user_obj.save()

        instance.loan_return = date.today()
        instance.save()

        return instance

    id = serializers.UUIDField(read_only=True)
    copy = CopySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    loan_withdraw = serializers.DateField(read_only=True)
    loan_estimate_return = serializers.DateField(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "copy",
            "user",
            "loan_withdraw",
            "loan_estimate_return",
            "loan_return",
        ]
