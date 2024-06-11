from django.shortcuts import render

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import Restaurant, RestaurantCategory, RoomType, RestaurantRoom, RestaurantMenu, Comment
from .serializers import (CategorySerializer, RestaurantSerializer,
                          RoomSerializer, RoomTypeSerializer, MenuSerializer, CommentSerializer)
from .permission import IsOwner


# RESTAURANT SECTION

class RestaurantFilterViewSet(ViewSet):
    permission_classes = [AllowAny]
    def restaurant_filter_view(self, request, *args, **kwargs):
        params = kwargs
        restaurants = Restaurant.objects.filter(restaurant_name=params['pk'])
        restaurants_serialize = RestaurantSerializer(restaurants, many=True).data
        return Response(data={'Result': restaurants_serialize}, status=status.HTTP_200_OK)

    def show_restaurant(self, request):
        restaurant_info = Restaurant.objects.all()
        restaurant_serialize = RestaurantSerializer(restaurant_info, many=True).data
        return Response(data={"List of restaurants": restaurant_serialize}, status=status.HTTP_200_OK)


# done
class RestaurantCategoryViewSet(ViewSet):
    permission_classes = [AllowAny]
    def restaurant_category(self, request):
        category = RestaurantCategory.objects.all()
        category_serialize = CategorySerializer(category, many=True).data
        return Response(data={"list of categories": category_serialize}, status=status.HTTP_200_OK)


# done
class RestaurantViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsOwner]

    def add_restaurant(self, request):
        # author = request.user
        category = RestaurantCategory.objects.filter(id=request.data['category_id'])
        restaurant_obj = Restaurant.objects.create(restaurant_name=request.data['restaurant_name'],
                                                   picture=request.data['picture'],
                                                   description=request.data['description'],
                                                   address=request.data['address'], phone=request.data['phone'],
                                                   email=request.data['email'], service_fee=request.data['service_fee'],
                                                   category=category)
        restaurant_obj.save()
        return Response(data={'message': 'Restaurant successfully created'}, status=status.HTTP_201_CREATED)

# done
class ActionRestaurantViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def show_restaurant_detail(self, request, pk):
        restaurant_detail = Restaurant.objects.filter(id=pk).first()
        restaurant_serialize = RestaurantSerializer(restaurant_detail).data
        return Response(data={"restaurant_detail": restaurant_serialize}, status=status.HTTP_200_OK)

    # Need to fix.
    def edit_restaurant(self, request, pk):
        obj = Restaurant.objects.filter(id=pk).first()
        serializer = RestaurantSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

    def delete_restaurant(self, request, pk):
        restaurant = Restaurant.objects.filter(id=pk).first()
        message = f"{restaurant.restaurant_name} was deleted"
        del restaurant
        return Response(data={"message": message}, status=status.HTTP_200_OK)


# ROOM SECTION.

class RoomTypeViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def add_room_type(self, request):
        room_type = RoomType.objects.create(room_type_name=request.data['room_type_name'])
        room_type.save()
        return Response(data={"message": f"{room_type} type is created successfully"}, status=status.HTTP_201_CREATED)

    def show_room_type(self, request):
        room_type = RoomType.objects.all()
        room_type_serialize = RoomTypeSerializer(room_type, many=True).data
        return Response(data={"list of room types": room_type_serialize}, status=status.HTTP_200_OK)


class RoomTypeActionViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    # Need to fix
    def edit_room_type(self, request, pk):
        obj = RoomType.objects.filter(id=pk).first()
        serializer_type = RoomTypeSerializer(obj, data=request.data, partial=True).data
        if serializer_type.is_valid():
            serializer_type.save()


    def delete_room_type(self, request, pk):
        room_type = RoomType.objects.filter(id=pk).first()
        message = f"{room_type} type was deleted"
        del room_type
        return Response(data={"message": message}, status=status.HTTP_200_OK)


class RestaurantRoomViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    """
    Restaurantlarni room lari ni royxat korinishda olish uchun

    Diqqat: {id} - restaurant id si jonatilish shart
    Talab qilinmaydi: User ixtiyoriy bolishi kerak, royxatdan otgan otmagan, admin admin emas ...
    """

    def add_room(self, request):
        room = RestaurantRoom.objects.create(
            restaurant=Restaurant.objects.filter(id=request.data['restaurant_id']).first(),

            room_name=request.data['room_name'],
            pictures=request.data['pictures'],
            description=request.data['description'],
            people_number=request.data['people_number'],
            waiters_number=request.data['waiters_number'],
            room_type=RoomType.objects.filter(id=request.data['room_type_id']).first(), )
        room.save()
        return Response(data={"message": f"{room} room is created successfully"}, status=status.HTTP_201_CREATED)

    def show_restaurant_room(self, request, pk):
        room = RestaurantRoom.objects.filter(restaurant_id=pk)
        room_serialize = RoomSerializer(room, many=True).data
        return Response(data={"list of rooms": room_serialize}, status=status.HTTP_200_OK)


class RestaurantRoomActionViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    """
    Restaurant uchun yangi room qoshish uchun ishlatiladi.

    Diqqat: {id} - restaurant id si jonatilish shart
    Talab qilinadi: User restaurant egasi, yoki tizim adminstratori bolishi kerak
    """

    def show_room_detail(self, request, pk):
        room = RestaurantRoom.objects.filter(restaurant_id=pk).first()
        room_serialize = RoomSerializer(room, many=True).data
        return Response(data={"room_details": room_serialize}, status=status.HTTP_200_OK)

    # Need to fix.
    def edit_room(self, request, pk):
        obj = RestaurantRoom.objects.filter(id=pk).first()
        serializer_room = RoomSerializer(obj, data=request.data, partial=True).data
        if serializer_room.is_valid():
            serializer_room.save()

    def delete_room(self, request, pk):
        room = RestaurantRoom.objects.filter(id=pk).first()
        message = f"{room} was deleted"
        del room
        return Response(data={"message": message}, status=status.HTTP_200_OK)


# Menu section

class RestaurantMenuViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def show_restaurant_menu(self, request):
        menu = RestaurantMenu.objects.filter(restaurant_id=request.data['restaurant_id'])
        menu_serialize = MenuSerializer(menu, many=True).data
        return Response(data={"menu": menu_serialize}, status=status.HTTP_200_OK)

    def add_restaurant_menu(self, request):
        menu = RestaurantMenu.objects.create(restaurant_id=request.data['restaurant_id'],
                                             name=request.data['name'],
                                             pictures=request.data['pictures'],
                                             price=request.data['price'],
                                             ingredients=request.data['ingredients'],
                                             description=request.dadta['description'],
                                             )
        menu.save()
        message = f"{menu.name} is created successfully"
        return Response(data={"message": message}, status=status.HTTP_201_CREATED)


class RestaurantMenuActionsView(ViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    def show_menu_detail(self, request, pk):
        menu = RestaurantMenu.objects.filter(id=pk).first()
        menu_serialize = MenuSerializer(menu, many=True).data
        return Response(data={"menu_details": menu_serialize}, status=status.HTTP_200_OK)

    # Need to fix.
    def edit_menu(self, request, pk):
        obj = RestaurantMenu.objects.filter(id=pk).first()
        serializer_menu = MenuSerializer(obj, data=request.data, partial=True).data
        if serializer_menu.is_valid():
            serializer_menu.save()

    def delete_menu(self, request, pk):
        menu = RestaurantMenu.objects.filter(id=pk).first()
        message = f"{menu.name} is deleted"
        del menu
        return Response(data={"message": message}, status=status.HTTP_200_OK)


# Comments and Reviews

class CommentViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, restaurant_id):
        comments = Comment.objects.filter(restaurant_id=restaurant_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(data={"message": "Comment successfully added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def restaurant_rate_view(request):
    pass
