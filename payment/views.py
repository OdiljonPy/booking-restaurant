from rest_framework.viewsets import ViewSet
from .utils import pan_checker
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import PaymentSerializer
#  from booking.models import Booking  # add after booking changed
from swagger_schema.Request import PaymentSwagSerializer


class PaymentViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create PaymentHistory',
        operation_description='Create PaymentHistory Data',
        request_body=PaymentSwagSerializer,
        responses={201: PaymentSwagSerializer()},
        tags=['Payment']
    )
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "Register first, then you can pay!"},
                            status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        pan_checker(data.get('pan', ''))
        data['user'] = user.id
        data['booking_id'] = data.get('booking_id')  # will be deleted after booking changed
        data['amount'] = data.get('amount')  # will be deleted after booking changed

        """
        # booking_id = data.get('booking_id')
        # booking = Booking.objects.filter(id=booking_id, user=user).first()
        # if booking is None:
        #     return Response({"message": "Booking did not created yet"},
        #                     status=status.HTTP_404_NOT_FOUND)
        # 
        # data['amount'] = booking.total_sum
        """

        payment_serializer = PaymentSerializer(data=data)
        if payment_serializer.is_valid():
            payment_serializer.save()
            return Response({"message": "Your payment data sent to GateWay, imagine they sent us respond -> 'ok'",
                             "status": status.HTTP_201_CREATED})
        else:
            return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
