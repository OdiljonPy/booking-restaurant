import requests
from rest_framework.viewsets import ViewSet
from .utils import pan_changer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import PaymentSerializer
from booking.models import Booking


class PaymentViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create PaymentDetail',
        operation_description='Create PaymentDetail data',
        request_body=PaymentSerializer(),
        responses={201: PaymentSerializer()},
        tags=['Payment']
    )
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        data['pan'] = pan_changer(data.get('pan'))
        booking_id = data.get('booking_id')
        booking = Booking.objects.filter(id=booking_id).first()
        amount = booking.total_sum
        data['amount'] = amount
        data['user'] = user

        """response = requests.post('hhtps://paycom.uz/api/v1/payment', json={"pan": ..., ...})
        if ...:
            pay_data_obj = PaymentWithHistory.objects.create(user=user, order_id=order_id, pan=pan,
                                                            expire_month=expire_month, status='1')
            pay_data_obj.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            ...
            """
        if booking is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        payment_serializer = PaymentSerializer(data=data)

        if payment_serializer.is_valid():
            payment_serializer.save()
            return Response({"message": "Your payment data sent to GateWay, imagine they sent us respond -> 'ok'",
                             "status": status.HTTP_201_CREATED})
        else:
            return Response({"message": "Fill the required columns"}, status=status.HTTP_400_BAD_REQUEST)



