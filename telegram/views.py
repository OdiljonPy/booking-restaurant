from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet

from .serializer import TelegramUserSerializer, RestSerializer, ResCategorySerializer, RestaurantRoomSerializer, \
    RoomsTypeSerializer, MenuTypeSerializer, RestaurantMenuSerializer, AllRestaurantSerializer
from .utils import telegram_add
from .models import TelegramUser
from restaurants.models import Restaurant, RestaurantCategory, RoomType, RestaurantRoom, RestaurantMenu, MenuType


class TelegramUserViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='User creating',
        responses={201: TelegramUserSerializer(), 400: 'Bad Request'},
    )
    def create(self, request):
        data = request.data

        user = TelegramUser.objects.filter(user_id=data['telegram_id']).first()
        if user is None:
            serializer = TelegramUserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                obj = TelegramUser.objects.create(user_id=request.data['telegram_id'],
                                                  first_name=request.data['first_name'],
                                                  last_name=request.data['last_name'],
                                                  username=request.data['username'], phone=request.data['phone'])

                obj.save()
                telegram_add(obj)
                return Response('User created', status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': "User already exists"}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='See all restaurants',
        responses={200: AllRestaurantSerializer()},
    )
    def all_restaurants(self, request):
        restaurants = Restaurant.objects.all()
        serializer = AllRestaurantSerializer(restaurants, many=True)
        return Response(data={'List_Restaurants': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Information for each restaurants',
        responses={200: RestSerializer()},
    )
    def filter_restaurant(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestSerializer(restaurants, many=True).data
        return Response(data={'Restaurants': serializer}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Category restaurants',
        responses={200: ResCategorySerializer()}
    )
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
