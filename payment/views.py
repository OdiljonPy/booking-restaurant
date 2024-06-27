from rest_framework.viewsets import ViewSet
from utils import pan_changer
from rest_framework.response import Response
from rest_framework import status
from .models import PaymentWithHistory
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import PaymentSerializer


class PaymentViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=PaymentSerializer(),
        responses={201: openapi.Response(description='Successful')}
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            data = request.data
            pan = pan_changer(data.get('pan'))
            expire_month = data.get('expire_month')
            order_id = data.get('order_id')
            pay_data_obj = PaymentWithHistory.objects.create(user=user, order_id=order_id, pan=pan,
                                                             expire_month=expire_month, status='1')
            pay_data_obj.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
