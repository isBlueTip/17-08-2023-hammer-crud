from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .services import generate_invite_code, validate_phone


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, validators=(validate_phone,))
    otp = models.CharField(max_length=4)
    invite_code = models.CharField(max_length=6, unique=True, null=True)
    referred_by = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f"{self.username} | {self.phone_number}"

    @receiver(pre_save)
    def populate_invite_code(sender, instance, *args, **kwargs):
        if instance.invite_code:
            return
        while True:
            invite_code = generate_invite_code()
            if not User.objects.filter(invite_code=invite_code).exists():
                break
        instance.invite_code = invite_code
