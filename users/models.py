import time
from random import choices

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    auth_code = models.CharField(max_length=4)
    invite_code = models.CharField(max_length=6, unique=True, null=True)
    referred_by = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f"{self.username} | {self.phone_number}"

    @staticmethod
    def generate_otp():
        time.sleep(2)
        return "".join(choices("0123456789", k=4))
