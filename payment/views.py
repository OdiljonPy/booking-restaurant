from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Cards, OTP, Booking
from .utils import send_otp
from datetime import datetime, timedelta


class OTPViewSet(ViewSet):
    def send(self, request):
        card_obj = Cards.objects.filter(pan=request.data['pan'], expire_year=request.data['expire_year'],
                                        expire_month=request.data['expire_month']).first()
        if card_obj is None:
            return Response(data={'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)

        otp = OTP.objects.create(phone_number=card_obj.phone_number)
        otp.save()
        send_otp(otp)
        return Response(data={'otp_key': otp.otp_key, 'created_at': otp.created_at}, status=status.HTTP_201_CREATED)

    def verify(self, request):
        otp_key = request.data['otp_key']
        otp_code = request.data['otp_code']
        otp = OTP.objects.filter(otp_key=otp_key, otp_code=otp_code).first()
        if otp is None:
            return Response(data={'error': 'OTP not found'}, status=status.HTTP_404_NOT_FOUND)
        if (otp.created_at - datetime.now()) > timedelta(minutes=3):
            return Response(data={'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

        card = Cards.objects.filter(phone_number=otp.phone_number).first()
        otp.delete()
        return Response(data={'card_token': card.token}, status=status.HTTP_200_OK)


class PaymentViewSet(ViewSet):
    def pay(self, request):
        card_obj = Cards.objects.filter(pan=request.data['pan'], expire_year=request.data['expire_year'],
                                        expire_month=request.data['expire_month']).first()

        if card_obj is None:
            return Response(data={'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)
        booking_id = request.data['booking_id']
        amount = card_obj.balance
        booking_price = Booking.objects.filter(id=booking_id)
        if amount >= booking_price:
            amount -= booking_price
            amount.save(update_fields=['amount'])
            return Response(data={'message': 'Your order booked successfully'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data={'message': 'You have not enough money for booking'},
                            status=status.HTTP_205_RESET_CONTENT)

