from rest_framework import serializers
from .models import Loan
import uuid


class LoanSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, read_only=True
    )
    loan_withdraw = serializers.DateField(read_only=True)

    class Meta:
        model = Loan
        fields = ["copy_id", "user_id", "loan_return"]
