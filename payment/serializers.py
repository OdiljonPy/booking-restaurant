from rest_framework.serializers import ModelSerializer
from .models import PaymentHistory


class OrderSerializer(ModelSerializer):
    class Meta:
        model = PaymentHistory
        exclude = ['created_at', 'updated_at']



