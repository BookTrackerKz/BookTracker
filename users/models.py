from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=127, unique=True)
    username = models.CharField(max_length=50, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    number_loans = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    cleared_date = models.DateField(auto_now=True)
