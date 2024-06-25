from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .models import OTP


class OTPSerializer(Serializer):
    otp_key = serializers.IntegerField()
    otp_code = serializers.IntegerField()


class PanSerializer(Serializer):
    pan = serializers.IntegerField()
