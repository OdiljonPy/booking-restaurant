from payme.views import MerchantAPIView
from rest_framework.generics import CreateAPIView
from .models import PaymentHistory
from payme.models import MerchantTransactionsModel
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from payme.methods.generate_link import GeneratePayLink


class PaymeCallBackAPIView(MerchantAPIView):
    def create_transaction(self, order_id, action, *args, **kwargs) -> None:
        print(f"create_transaction for order_id: {order_id}, response: {action}")
        transaction = MerchantTransactionsModel.objects.filter(id=action['result']['transaction'])
        if transaction.exists():
            order = PaymentHistory.objects.filter(id=order_id)
            order.status = PaymentHistory.Status.PENDING
            order.save(update_fields=['status'])

    def perform_transaction(self, order_id, action, *args, **kwargs) -> None:
        print(f"perform_transaction for order_id: {order_id}, response: {action}")
        transaction = MerchantTransactionsModel.objects.filter(id=action['result']['transaction'])
        if transaction.exists():
            order = PaymentHistory.objects.filter(id=order_id)
            order.status = PaymentHistory.Status.PAID
            order.save(update_fields=['status'])

    def cancel_transaction(self, order_id, action, *args, **kwargs) -> None:
        print(f"cancel_transaction for order_id: {order_id}, response: {action}")
        transaction = MerchantTransactionsModel.objects.filter(id=action['result']['transaction'])
        if transaction.exists():
            order = PaymentHistory.objects.filter(id=order_id)
            order.status = PaymentHistory.Status.CANCELED
            order.save(update_fields=['status'])


class OrderStatusApiView(CreateAPIView):
    queryset = PaymentHistory.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid()
            self.perform_create(serializer)

            pay_link = GeneratePayLink(
                order_id=serializer.data['id'],
                amount=serializer.data['amount'],
                callback_url=settings.PAYME['PAYME_CALL_BACK_URL']
            ).generate_link()

            data = {
                'link': pay_link,
                'order': serializer.data,
            }
            return Response(data=data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(data={'message': 'Your data is invalid'}, status=status.HTTP_400_BAD_REQUEST)
