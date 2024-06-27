from rest_framework import serializers
from .models import PaymentWithHistory


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentWithHistory
        fields = ['pan', 'expire_month', 'booking_id', 'amount', 'user']
