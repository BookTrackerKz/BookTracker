from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=127, unique=True)
    username = models.CharField(max_length=50, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    number_loans = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0
    )
    cleared_date = models.DateField()

    loan = models.ManyToManyField(
        "copies.Copy", through="users.Loan", related_name="users_loan"
    )


class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan_withdraw = models.DateField(auto_now_add=True)
    loan_return = models.DateField(null=True, default=None)
    loan_estimate_return = models.DateField()

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_loans"
    )
    copy = models.ForeignKey(
        "copies.Copy", on_delete=models.CASCADE, related_name="copy_loans"
    )
