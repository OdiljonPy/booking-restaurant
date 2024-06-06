import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from authentication.utils import generate_otp_code


class User(AbstractUser):
    email = False
    username = models.CharField(max_length=14, unique=True)


class OTP(models.Model):
    phone_number = models.CharField(max_length=14, unique=True)
    otp_code = models.IntegerField(default=generate_otp_code)
    otp_key = models.UUIDField(default=uuid.uuid4, unique=True)

    expire_data = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.otp_key
