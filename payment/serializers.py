from rest_framework import serializers
from rest_framework.serializers import Serializer
from .utils import is_valid_pan, is_valid_month


class PaymentSerializer(Serializer):
    order_id = serializers.IntegerField()
    pan = serializers.CharField(max_length=16, validators=[is_valid_pan])
    expire_month = serializers.CharField(max_length=2, validators=[is_valid_month])
