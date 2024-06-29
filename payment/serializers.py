from rest_framework import serializers
from .models import PaymentWithHistory


#
#
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentWithHistory
        fields = ['user', 'pan', 'expire_month', 'amount', 'booking_id']

