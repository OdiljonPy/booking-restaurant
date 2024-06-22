import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from authentication.utils import generate_otp_code
from authentication.validations import validate_uz_number


class User(AbstractUser):
    username = models.CharField(max_length=14, unique=True, validators=[validate_uz_number])
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.IntegerField(default=generate_otp_code)
    otp_key = models.UUIDField(default=uuid.uuid4)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
