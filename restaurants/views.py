from drf_yasg.utils import swagger_auto_schema

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from .error_codes import ErrorCodes
from .exception import CustomApiException

from .models import Restaurant, RestaurantCategory, RoomType, RestaurantRoom, RestaurantMenu, Comment, MenuType
from .serializers import (CategorySerializer, RestaurantSerializer,
                          RoomSerializer, RoomTypeSerializer, MenuSerializer, CommentSerializer,
                          RestaurantCreateSerializer, RoomCreateSerializer, MenuCreateSerializer,
                          CategoryCreateSerializer, RoomTypeCreateSerializer, MenuTypeCreateSerializer,
                          MenuTypeSerializer)
from .permission import IsOwner

from difflib import SequenceMatcher


# TODO: need to write filter for restaurant
class RestaurantFilterViewSet(ViewSet):

    @swagger_auto_schema(
        operation_summary='Show restaurants',
        operation_description='Show restaurants list',
        responses={200: CategorySerializer()},
        tags=['Restaurant']
    )
    def show_restaurant(self, request):
        restaurant_info = Restaurant.objects.all()
        restaurant_serialize = RestaurantSerializer(restaurant_info, many=True).data
        return Response(data={"List of restaurants": restaurant_serialize}, status=status.HTTP_200_OK)


class RestaurantCategoryViewSet(ViewSet):

    @swagger_auto_schema(
        operation_description="Create Restaurant",
        operation_summary="Create Restaurant",
        request_body=CategoryCreateSerializer,
        responses={201: CategoryCreateSerializer()},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def create_category(self, request):
        category_serializer = CategoryCreateSerializer(data=request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(data={"result": "Category added successfully"}, status=status.HTTP_201_CREATED)
        return Response(data={"result": "please add the category name"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Show categories',
        operation_description='Show Restaurant categories list',
        responses={200: CategorySerializer()},
        tags=['Restaurant']
    )
    # @permission_classes([AllowAny])
    def restaurant_category(self, request):
        category = RestaurantCategory.objects.all()
        category_serialize = CategorySerializer(category, many=True).data
        return Response(data={"result": category_serialize}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Delete Category',
        operation_description='Delete Restaurant Category',
        responses={204: 'Category successfully deleted'},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def delete_category(self, request, pk):
        category = RestaurantCategory.objects.filter(pk=pk).first()
        if category:
            message = f"{category} was deleted successfully"
            category.delete()
            return Response(data={"result": message}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={"result": "Category doesn't find"}, status=status.HTTP_404_NOT_FOUND)


class RestaurantViewSet(ViewSet):

    @swagger_auto_schema(
        operation_summary='Create Restaurant',
        operation_description='Create Restaurant',
        request_body=RestaurantCreateSerializer,
        responses={201: 'Restaurant successfully created'},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def add_restaurant(self, request):
        restaurant_obj = RestaurantCreateSerializer(data=request.data)
        if restaurant_obj.is_valid():
            restaurant_obj.save()
            return Response(data={'result': restaurant_obj.data}, status=status.HTTP_201_CREATED)
        return Response(data={'result': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Show Restaurant',
        operation_description='Show Restaurant Info',
        responses={200: RestaurantSerializer()},
        tags=['Restaurant']
    )
    # @permission_classes([AllowAny])
    def show_restaurant_detail(self, request, pk):
        restaurant_detail = Restaurant.objects.filter(id=pk).first()
        restaurant_serialize = RestaurantSerializer(data=restaurant_detail).data
        return Response(data={"restaurant_detail": restaurant_serialize}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Edit Restaurant',
        operation_description='Edit Restaurant Info',
        responses={200: RestaurantSerializer(), 202: RestaurantSerializer(), 400: 'Invalid request',
                   404: 'Restaurant does not exist'},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def edit_restaurant(self, request, pk):
        obj = Restaurant.objects.filter(id=pk).first()
        serializer = RestaurantSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"result": serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response(data={"result": "Data doesn't found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary='Delete Restaurant',
        operation_description='Delete Restaurant Info',
        responses={204: "Restaurant successfully deleted"},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def delete_restaurant(self, request, pk):
        restaurant = Restaurant.objects.filter(id=pk).first()
        message = f"{restaurant.restaurant_name} was deleted"
        restaurant.delete()
        return Response(data={"message": message}, status=status.HTTP_204_NO_CONTENT)


class RoomTypeViewSet(ViewSet):

    @swagger_auto_schema(
        operation_summary='Create Room Type',
        operation_description='Create Room Type',
        request_body=RoomTypeCreateSerializer,
        responses={201: 'Restaurant successfully created'},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def add_room_type(self, request):
        room_type = RoomTypeCreateSerializer(data=request.data)
        if room_type.is_valid():
            room_type.save()
            return Response(data={'result': room_type.data}, status=status.HTTP_201_CREATED)
        return Response(data={'result': 'Invalid serializer'}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Show Room Type',
        operation_description='Show Room Type',
        responses={200: RoomTypeSerializer()},
        tags=['Restaurant']
    )
    # @permission_classes([AllowAny])
    def show_room_type(self, request):
        room_type = RoomType.objects.all()
        room_type_serialize = RoomTypeSerializer(room_type, many=True).data
        return Response(data={"result": room_type_serialize}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Edit Room Type',
        operation_description='Edit Restaurant Room Type',
        responses={200: RoomTypeSerializer(), 202: RoomTypeSerializer(), 400: 'Invalid request',
                   404: 'Room type does not exist'},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def edit_room_type(self, request, pk):
        obj = RoomType.objects.filter(id=pk).first()
        serializer_type = RoomTypeSerializer(obj, data=request.data, partial=True)
        if serializer_type.is_valid():
            serializer_type.save()
            return Response(data={'result': serializer_type.data}, status=status.HTTP_202_ACCEPTED)
        return Response(data={'result': 'Serializer is invalid'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Delete Room Type',
        operation_description='Delete Room Type',
        responses={204: "Room type successfully deleted"},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def delete_room_type(self, request, pk):
        room_type = RoomType.objects.filter(id=pk).first()
        message = f"{room_type} type was deleted"
        room_type.delete()
        return Response(data={"message": message}, status=status.HTTP_204_NO_CONTENT)


class RestaurantRoomViewSet(ViewSet):

    @swagger_auto_schema(
        operation_summary='Create Room',
        operation_description='Create Restaurant Room',
        request_body=RoomCreateSerializer,
        responses={201: 'Restaurant room successfully created'},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def add_room(self, request, pk):
        room = RoomCreateSerializer(data=request.data)
        if room.is_valid():
            room.save()
            return Response(data={"result": room.data}, status=status.HTTP_201_CREATED)
        return Response(data={'result': 'Invalid serializer'}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Show Restaurant',
        operation_description='Show Restaurant Info',
        responses={200: RoomSerializer()},
        tags=['Restaurant']
    )
    # @permission_classes([AllowAny])
    def show_restaurant_room(self, request, pk):
        room = RestaurantRoom.objects.filter(restaurant_id=pk)
        room_serialize = RoomSerializer(room, many=True).data
        return Response(data={"list of rooms": room_serialize}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Show Room',
        operation_description='Show Restaurant Room detail Info',
        responses={200: RoomSerializer()},
        tags=['Restaurant']
    )
    # @permission_classes([AllowAny])
    def show_room_detail(self, request, pk):
        room = RestaurantRoom.objects.filter(restaurant_id=pk).first()
        room_serialize = RoomSerializer(room, many=True).data
        return Response(data={"room_details": room_serialize}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Edit Room',
        operation_description='Edit Restaurant Room',
        responses={200: RoomSerializer(), 202: RoomSerializer(), 400: 'Invalid request',
                   404: 'Room type does not exist'},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def edit_room(self, request, pk):
        obj = RestaurantRoom.objects.filter(id=pk).first()
        serializer_room = RoomSerializer(obj, data=request.data, partial=True)
        if serializer_room.is_valid():
            serializer_room.save()
            return Response(data={'message': serializer_room.data}, status=status.HTTP_202_ACCEPTED)
        return Response(data={'message': 'Serializer is invalid'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Delete Room',
        operation_description='Delete Room',
        responses={204: "Room successfully deleted"},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def delete_room(self, request, pk):
        room = RestaurantRoom.objects.filter(id=pk).first()
        message = f"{room} was deleted"
        del room
        return Response(data={"message": message}, status=status.HTTP_200_OK)


class MenuTypeViewSet(ViewSet):

    @swagger_auto_schema(
        operation_summary='Create Menu Type',
        operation_description='Create Restaurant Menu Type',
        request_body=MenuTypeCreateSerializer(),
        responses={201: 'Restaurant menu type successfully created', 400: 'Invalid request'},
        tags=['Restaurant']
    )
    def add_menu_type(self, request):
        menu_type = MenuType.objects.all()
        serializer = MenuTypeCreateSerializer(menu_type, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'result': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(data={'result': 'Invalid serializer'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Show Menu Type',
        operation_description='Show Restaurant menu type',
        responses={200: RoomSerializer()},
        tags=['Restaurant']
    )
    def show_menu_type(self):
        meny_type = MenuType.objects.all()
        serializer = MenuTypeSerializer(meny_type, many=True).data
        return Response(data={'result': serializer}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Edit Menu type',
        operation_description='Edit Restaurant Meny Type',
        responses={200: MenuTypeSerializer(), 202: MenuTypeSerializer(), 400: 'Invalid request',
                   404: 'Menu type does not exist'},
        tags=['Restaurant']
    )
    def edit_menu_type(self, request, pk):
        menu_type = MenuType.objects.filter(id=pk).first()
        serializer = MenuTypeSerializer(menu_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'result': serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response(data={'result': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Delete Menu type',
        operation_description='Delete Menu type',
        responses={204: "Menu type successfully deleted"},
        tags=['Restaurant']
    )
    def delete_menu_type(self, request, pk):
        menu_type = MenuType.objects.filter(id=pk).first()
        message = f"{menu_type} type was deleted"
        menu_type.delete()
        return Response(data={'result': message}, status=status.HTTP_204_NO_CONTENT)


class RestaurantMenuViewSet(ViewSet):

    @swagger_auto_schema(
        operation_summary='Show Menu',
        operation_description='Show Restaurant menu',
        responses={200: MenuSerializer()},
        tags=['Restaurant']
    )
    # @permission_classes([AllowAny])
    def show_restaurant_menu(self, request):
        menu = RestaurantMenu.objects.filter(restaurant_id=request.data['restaurant_id'])
        menu_serialize = MenuSerializer(menu, many=True).data
        return Response(data={"result": menu_serialize}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Create Menu',
        operation_description='Create Restaurant Menu',
        request_body=MenuSerializer(),
        responses={201: 'Restaurant menu successfully created'},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def add_restaurant_menu(self, request):
        menu = MenuCreateSerializer(data=request.data)
        if menu.is_valid():
            menu.save()
            return Response(data={"result": menu.data}, status=status.HTTP_201_CREATED)
        return Response(data={"result": 'Serializer is invalid'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Show Menu detail',
        operation_description='Show Restaurant menu detail',
        responses={200: MenuSerializer()},
        tags=['Restaurant']
    )
    # @permission_classes([AllowAny])
    def show_menu_detail(self, request, pk):
        menu = RestaurantMenu.objects.filter(id=pk).first()
        menu_serialize = MenuSerializer(menu, many=True).data
        return Response(data={"result": menu_serialize}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Edit Menu',
        operation_description='Edit Restaurant Menu',
        responses={200: MenuSerializer(), 202: MenuSerializer(), 400: 'Invalid request',
                   404: 'Menu does not exist'},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def edit_menu(self, request, pk):
        obj = RestaurantMenu.objects.filter(id=pk).first()
        serializer_menu = MenuSerializer(obj, data=request.data, partial=True)
        if serializer_menu.is_valid():
            serializer_menu.save()
            return Response(data={'result': serializer_menu.data}, status=status.HTTP_202_ACCEPTED)
        return Response(data={'result': 'Serializer is invalid'})

    @swagger_auto_schema(
        operation_summary='Delete Menu',
        operation_description='Delete Menu',
        responses={204: "Menu successfully deleted"},
        tags=['Restaurant']
    )
    # @permission_classes([IsAuthenticated])
    def delete_menu(self, request, pk):
        menu = RestaurantMenu.objects.filter(id=pk).first()
        message = f"{menu.name} is deleted"
        del menu
        return Response(data={"message": message}, status=status.HTTP_200_OK)


class CommentViewSet(ViewSet):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Show Comment list',
        operation_description='Show Restaurant Comment list',
        responses={200: CommentSerializer()},
        tags=['Restaurant']
    )
    def comment_list(self, request, restaurant_id):
        comments = Comment.objects.filter(restaurant_id=restaurant_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def comment_create(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(data={"message": "Comment successfully added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
