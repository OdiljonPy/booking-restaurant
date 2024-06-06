from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.models import User, OTP
from .serializers import UserSerializer
from .utils import send_opt


@api_view(['GET'])
def auth_me(request):
    if request.user.is_authenticated:
        return Response(data=UserSerializer(request.user).data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class OTPViewSet(ViewSet):

    def send(self, request):
        print(request)
        print(request.user)
        user_obj = User.objects.filter(id=request.user.id).first()
        print("+" * 50)
        print(user_obj)
        print(user_obj.id)

        if user_obj is None:
            return Response(data={'error': 'user not found!'}, status=status.HTTP_404_NOT_FOUND)
        otp = OTP.objects.create(phone_number=user_obj.id)
        otp.save()
        send_opt(otp)
        return Response(data={'otp_key': otp.otp_key, 'created_at': otp.created_at}, status=status.HTTP_201_CREATED)

    def verify(self, request):
        pass

