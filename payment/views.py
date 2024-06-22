from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Card, OTP
from .utils import send_otp, number_of_otp
from booking.models import Booking
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import OTPSerializer, PanSerializer
from drf_yasg.utils import swagger_auto_schema
from restaurants.models import Restaurant


class OTPViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="info",
        operation_summary="Card pan number",
        responses={201: OTPSerializer()},
        request_body=PanSerializer(),
        tags=['payment']
    )
    def send(self, request):
        card_obj = Card.objects.filter(pan=request.data['pan']).first()
        if card_obj is None:
            return Response(data={'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)
        order_obj = Booking.objects.filter(id=request.data['booking_id']).first()
        if order_obj is None:
            return Response(data={'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        if card_obj.balance < order_obj.total_sum:
            return Response(data="You have not enough money", status=status.HTTP_400_BAD_REQUEST)

        otp = OTP.objects.create(phone_number=card_obj.phone_number)
        if not number_of_otp(otp):
            return Response(data={'message': 'Try again 10 hours later'}, status=status.HTTP_400_BAD_REQUEST)
        if number_of_otp(otp) == 'delete':
            serializer = OTPSerializer(otp, data={"deleted_at": datetime.now()}, many=True)
            serializer.save()

        otp.save()
        send_otp(otp)
        return Response(data={'otp_key': otp.otp_key, 'created_at': otp.created_at}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="verify",
        operation_summary="verify transaction",
        responses={201: "Status message"},
        request_body=OTPSerializer(),
        tags=['payment']
    )
    def verify(self, request):
        otp_key = request.data['otp_key']
        otp_code = request.data['otp_code']
        booking_id = request.data['booking_id']
        otp = OTP.objects.filter(otp_key=otp_key, otp_code=otp_code).first()
        if otp is None:
            return Response(data={'error': 'OTP not found'}, status=status.HTTP_404_NOT_FOUND)
        if (datetime.now() - otp.created_at) > timedelta(minutes=3):
            return Response(data={'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

        card = Card.objects.filter(phone_number=otp.phone_number).first()
        order = Booking.objects.filter(id=booking_id).first()
        card.balance = card.balance - order.total_sum
        card.save(update_fields=['balance'])

        # Restaurant balance ga o'tkazilgan pul miqdorini qo'shish kerak.
        # Restaurant ni order orqali saralab ololmadim.

        otp.delete()
        return Response(data={'card_balance': card.balance,
                              'Transaction amount': order.total_sum}, status=status.HTTP_200_OK)

class PaymentViewSet(ViewSet):
    pass

# class PaymentViewSet(ViewSet):
#     def pay(self, request):
#         card_obj = Cards.objects.filter(pan=request.data['pan'], expire_year=request.data['expire_year'],
#                                         expire_month=request.data['expire_month']).first()
#         restaurant_obj = PaymentWithHistory.objects.filter(restaurants_id=request.data['restaurant_id']).first()
#         if restaurant_obj is None:
#             return Response(data={'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
#         if card_obj is None:
#             return Response(data={'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)
#         restaurant_balance = restaurant_obj.balance
#         booking_id = request.data['booking_id']
#         card_balance = card_obj.balance
#         booking_price = PaymentWithHistory.booking.objects.filter(id=booking_id).price
#         if card_balance >= booking_price:
#             card_balance -= booking_price
#             card_balance.save(update_fields=['balance'])
#             restaurant_balance += booking_price
#             restaurant_balance.save(update_fields=['balance'])
#             return Response(data={'message': 'Your order booked successfully'}, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(data={'message': 'You have not enough money for booking'},
#                             status=status.HTTP_205_RESET_CONTENT)

# class PaymentViewSet(ViewSet):
#     def pay(self, request):
#         token = request['token']
#         card = Cards.objects.filter(token=token).first()
#         restaurant = PaymentWithHistory.restaurant.objects.filter(id=request.data['restaurant_id']).first()
#         booking_id = request['booking_id']
#         booking_obj = PaymentWithHistory.booking.objects.filter(booking_id=booking_id).first()
#         if booking_obj is None:
#             return Response(data={'error': 'That booking not found'}, status=status.HTTP_404_NOT_FOUND)
#         if restaurant is None:
#             return Response(data={'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
#         if card is None:
#             return Response(data={'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)
#         restaurant_balance = restaurant.balance
#         card_balance = card.balance
#         if card.balance >= booking_obj.price:
#             card_balance -= booking_obj.price
#             restaurant_balance += booking_obj.price
#             card_balance.save(update_fields=['balance'])
#             restaurant_balance.save(update_fields=['balance'])
#         else:
#             return Response({'message': 'There is not enough money In your card!'})
