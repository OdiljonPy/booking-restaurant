import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import validate_uz_number


class User(AbstractUser):
    username = models.CharField(max_length=14, unique=True, validators=[validate_uz_number])
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.IntegerField(default=0)
    otp_key = models.UUIDField(default=uuid.uuid4, unique=True)

    expire_data = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class ChangePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
