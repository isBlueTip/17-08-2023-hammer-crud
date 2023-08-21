import datetime
import os

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .services import generate_invite_code, validate_phone


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True, validators=(validate_phone,))
    first_name = models.CharField("first name", max_length=150, blank=True)
    last_name = models.CharField("last name", max_length=150, blank=True)
    email = models.EmailField("email address", blank=True)
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    otp = models.CharField(max_length=4)
    invite_code = models.CharField(max_length=6, unique=True, null=True)
    referred_by = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f"{self.phone_number} | {self.first_name, self.last_name}"


@receiver(pre_save, sender=User)
def populate_users_invite_code(sender, instance, *args, **kwargs):
    if instance.invite_code:
        return
    while True:
        invite_code = generate_invite_code()
        if not User.objects.filter(invite_code=invite_code).exists():
            break
    instance.invite_code = invite_code
