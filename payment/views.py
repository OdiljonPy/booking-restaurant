from rest_framework.viewsets import ViewSet
from .utils import pan_checker, fine
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import PaymentSerializer
#  from booking.models import Booking  # add after booking changed
from .swagger_schema.request import PaymentSwagSerializer
from .models import PaymentWithHistory
import requests


#  from .models import PaymentWithHistory


class PaymentViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create PaymentHistory',
        operation_description='Create PaymentHistory Data',
        request_body=PaymentSwagSerializer,
        responses={201: PaymentSwagSerializer()},
        tags=['Payment']
    )
    def receive_money(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "Register first, then you can pay!",
                             'ok': False}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        pan_checker(data.get('pan'))
        data['user'] = user.id

        """
        # booking_id = data.get('booking_id')
        # booking = Booking.objects.filter(id=booking_id, user=user).first()
        # if booking is None:
        #     return Response({"message": "Booking did not created yet"},
        #                     status=status.HTTP_404_NOT_FOUND)
        # restaurant_id = booking.restaurant.id
        # 
        # data['amount'] = booking.total_sum
        """

        payment_serializer = PaymentSerializer(data=data)
        if not payment_serializer.is_valid():
            return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        payment_serializer.save()

        url = 'http://127.0.0.1:9000/api/v1/receive-money/'
        data = {
            # 'restaurant_id': restaurant_id,  # will be added later
            'pan': data['pan'],
            'amount': payment_serializer.data['amount']
        }
        response = requests.post(url, json=data)

        if response.status_code != 200:
            py_obj = PaymentWithHistory.objects.filter(id=payment_serializer.data.get('id')).first()
            py_obj.status = 3
            py_obj.save(update_fields=['status'])
            return Response({'error': 'Not enough money', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        py_obj = PaymentWithHistory.objects.filter(id=payment_serializer.data.get('id')).first()
        py_obj.status = 2
        py_obj.save(update_fields=['status'])
        data = {
            'message': 'Your payment created successfully',
            'ok': True
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

    def return_money(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'message': 'Do not registered yed', 'ok': False}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        pan_checker(data.get('pan'))
        data['user'] = user.id

        """
        booking_id = data.get('booking_id')
        booking = Booking.objects.filter(id=booking_id, user=user).first()
        if booking is None:
            return Response({"message": "Booking did not created yet"},
                            status=status.HTTP_404_NOT_FOUND)
        pay_history = PaymentWithHistory.objects.filter(booking_id=booking_id, status=2).first()
        if not pay_history:
            return Response({"message": "You did not pay yet to this order!}, status=status.HTTP_400_BAD_REQUEST)
        amount = pay_history.amount
        
        """
        payment_serializer = PaymentSerializer(data=data)
        if not payment_serializer.is_valid():
            return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        payment_serializer.save()
        amount = fine(payment_serializer.data['amount'])  # o'chirish kerak order bilan ishlash boshlangandan keyin.

        url = 'http://127.0.0.1:9000/api/v1/return-money/'
        data = {
            # 'restaurant_id': restaurant_id,  # will be added later Gateway uchun kerak
            'pan': data['pan'],
            'amount': amount
        }
        response = requests.post(url, json=data)

        if response.status_code != 200:
            py_obj = PaymentWithHistory.objects.filter(id=payment_serializer.data.get('id')).first()
            py_obj.status = 3
            py_obj.save(update_fields=['status'])
            return Response({'error': 'Not enough money to return, or have some issues with GateWay', 'ok': False},
                            status=status.HTTP_400_BAD_REQUEST)

        py_obj = PaymentWithHistory.objects.filter(id=payment_serializer.data.get('id')).first()
        py_obj.amount = amount
        py_obj.save(update_fields=['amount'])
        py_obj.status = 4
        py_obj.save(update_fields=['status'])
        data = {
            'message': 'Your money returned successfully, we kept a certain amount of fine money'
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
