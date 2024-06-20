from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet

from .serializer import TelegramUserSerializer
from .utils import telegram_code
from .models import TelegramUser


class TelegramUserViewSet(ViewSet):

    def create(self, request):
        data = request.data
        username = data['username']
        if TelegramUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TelegramUserSerializer(data=data)
        if serializer.is_valid():
            telegram_user = serializer.save()
            obj = TelegramUser.objects.create(user_id=telegram_user.id, first_name=request.data['first_name'],
                                              last_name=request.data['last_name'],
                                              username=request.data['username'], phone=request.data['phone'])

            obj.save()
            telegram_code(obj)
            return Response('User created', status=status.HTTP_201_CREATED)
