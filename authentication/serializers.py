import uuid

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import Serializer

from authentication.validations import validate_uz_number
from authentication.utils import generate_otp_code

from .models import User, OTP


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self, **kwargs):
        self.validated_data['password'] = make_password(self.validated_data['password'])
        return super().save(**kwargs)


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['otp_code', 'otp_key']


class ReSetPasswordSerializer(serializers.ModelSerializer):
    token = serializers.UUIDField()
    password = serializers.CharField(max_length=120)


class UserPasswordSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = [
            'password'
        ]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class LoginSerializer(Serializer):
    username = serializers.CharField(max_length=13, validators=[validate_uz_number, ])
    password = serializers.CharField(max_length=120)


class ResetUserPasswordSerializer(Serializer):
    username = serializers.CharField(max_length=13, validators=[validate_uz_number])


class OTPUserPasswordSerializer(Serializer):
    otp_code = serializers.IntegerField(default=generate_otp_code)
    otp_key = serializers.UUIDField(default=uuid.UUID)


class NewPasswordSerializer(Serializer):
    otp_token = serializers.UUIDField(default=uuid.uuid4)
    password = serializers.CharField(required=True)


class OTPResendSerializer(Serializer):
    otp_key = serializers.UUIDField(default=uuid.uuid4)
