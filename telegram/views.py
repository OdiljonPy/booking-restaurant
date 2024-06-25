from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet

from .serializer import TelegramUserSerializer, RestaurantSerializer, ResCategorySerializer, RestaurantRoomSerializer, \
    RoomsTypeSerializer, MenuTypeSerializer, RestaurantMenuSerializer
from .utils import telegram_add
from .models import TelegramUser
from restaurants.models import Restaurant, RestaurantCategory, RoomType, RestaurantRoom, RestaurantMenu, MenuType


class TelegramUserViewSet(ViewSet):

    def create(self, request):
        phone = request.data['phone']
        username = request.data['username']
        data = request.data
        if TelegramUser.objects.filter(phone=phone).exists():
            return Response(data={'error': 'This phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if TelegramUser.objects.filter(username=username).exists():
            return Response(data={'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TelegramUserSerializer(data=data)
        if serializer.is_valid():
            telegram_user = serializer.save()
            obj = TelegramUser.objects.create(user_id=telegram_user.id, first_name=request.data['first_name'],
                                              last_name=request.data['last_name'],
                                              username=request.data['username'], phone=request.data['phone'])

            obj.save()
            telegram_add(obj)
            return Response('User created', status=status.HTTP_201_CREATED)


class RestaurantViewSet(ViewSet):

    def all_restaurant(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True).data
        return Response(data={'Restaurants': serializer}, status=status.HTTP_200_OK)

    def category_restaurant(self, request):
        category = RestaurantCategory.objects.all()
        serializer = ResCategorySerializer(category, many=True).data
        return Response(data={'Categories': serializer}, status=status.HTTP_200_OK)


class RoomsViewSet(ViewSet):

    def room_type(self, request):
        rooms_type = RoomType.objects.all()
        serializer = RoomsTypeSerializer(rooms_type, many=True).data
        return Response(data={'Room Types': serializer}, status=status.HTTP_200_OK)

    def restaurant_room(self, request):
        restaurant_room = RestaurantRoom.objects.all()
        serializer = RestaurantRoomSerializer(restaurant_room, many=True).data
        return Response(data={'Restaurant Rooms': serializer}, status=status.HTTP_200_OK)


class RestMenuViewSet(ViewSet):  # RESTAURANT MENU

    def menu_type(self, request):
        menu_type = MenuType.objects.all()
        serializer = MenuTypeSerializer(menu_type, many=True).data
        return Response(data={'Menu Types': serializer}, status=status.HTTP_200_OK)

    def restaurant_menu(self, request):
        restaurant_menu = RestaurantMenu.objects.all()
        serializer = RestaurantMenuSerializer(restaurant_menu, many=True).data
        return Response(data={'Restaurant Menu': serializer}, status=status.HTTP_200_OK)
