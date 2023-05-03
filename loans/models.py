from django.db import models
import uuid


class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan_withdraw = models.DateField(auto_now_add=True)
    loan_return = models.DateField(null=True, default=None)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="loans"
    )
    copy = models.ForeignKey(
        "copies.Copy", on_delete=models.CASCADE, related_name="loans"
    )
