from drf_yasg.utils import swagger_auto_schema

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .exception import CustomApiException
from .error_codes import ErrorCodes
from .models import Restaurant, RestaurantCategory, RoomType, RestaurantRoom, RestaurantMenu, Comment, MenuType
from .serializers import (CategorySerializer, RestaurantSerializer,
                          RoomSerializer, RoomTypeSerializer, MenuSerializer, CommentSerializer,
                          RestaurantCreateSerializer, RoomCreateSerializer, MenuCreateSerializer,
                          CategoryCreateSerializer, RoomTypeCreateSerializer, MenuTypeCreateSerializer,
                          MenuTypeSerializer, CommentCreateSerializer)


class RestaurantCategoryViewSet(ViewSet):

    @swagger_auto_schema(
        operation_description="Create Restaurant category",
        operation_summary="Create Restaurant category",
        request_body=CategoryCreateSerializer,
        responses={201: CategoryCreateSerializer(), 400: 'Bad Request'},
        tags=['Restaurant']
    )
    def create_category(self, request):
        serializer = CategoryCreateSerializer(data=request.data)

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if serializer.is_valid():
            serializer.save()
            return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

        return Response(data={'result': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Show categories',
        operation_description='Show Restaurant categories list',
        responses={200: CategorySerializer(), 404: 'Not Found'},
        tags=['Restaurant']
    )
    def restaurant_category(self, request):
        category = RestaurantCategory.objects.all()

        if category:
            serializer = CategorySerializer(category, many=True)
            return Response(data={"result": serializer.data, 'ok': True}, status=status.HTTP_200_OK)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

    @swagger_auto_schema(
        operation_summary='Delete Category',
        operation_description='Delete Restaurant Category',
        responses={204: CategoryCreateSerializer, 400: 'Bad Request'},
        tags=['Restaurant']
    )
    #TODO: write new category delete serializer
    def delete_category(self, request):
        category = RestaurantCategory.objects.filter(id=request.data['category_id']).first()

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if category:
            message = f"{category} was deleted successfully"
            category.delete()
            return Response(data={"result": message, 'ok': True}, status=status.HTTP_204_NO_CONTENT)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)


class RestaurantViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create Restaurant',
        operation_description='Create Restaurant',
        request_body=RestaurantCreateSerializer,
        responses={201: 'Restaurant successfully created'},
        tags=['Restaurant']
    )
    def add_restaurant(self, request):
        data = request.data
        data['author'] = request.user.id
        serializer = RestaurantCreateSerializer(data=data)

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if serializer.is_valid():
            serializer.save()
            return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

        return Response(data={'result': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Show Restaurant',
        operation_description='Show Restaurant Info',
        responses={200: RestaurantSerializer(), 400: 'Bad request'},
        tags=['Restaurant']
    )
    def show_restaurant_detail(self, request, pk):
        restaurant = Restaurant.objects.filter(id=pk).first()

        if restaurant:
            serializer = RestaurantSerializer(restaurant, many=False)
            return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

    @swagger_auto_schema(
        operation_summary='Edit Restaurant',
        operation_description='Edit Restaurant Info',
        responses={200: RestaurantSerializer(), 202: RestaurantSerializer(), 400: 'Invalid request',
                   404: 'Restaurant does not exist'},
        tags=['Restaurant']
    )
    def edit_restaurant(self, request, pk):
        restaurant = Restaurant.objects.filter(id=pk).first()
        serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if serializer.is_valid():
            serializer.save()
            return Response(data={"result": serializer.data, 'ok': True}, status=status.HTTP_202_ACCEPTED)

        return Response(data={"result": serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Delete Restaurant',
        operation_description='Delete Restaurant Info',
        responses={204: "Restaurant successfully deleted"},
        tags=['Restaurant']
    )
    def delete_restaurant(self, request, pk):
        restaurant = Restaurant.objects.filter(id=pk).first()

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if restaurant:
            message = f"{restaurant.restaurant_name} was deleted"
            restaurant.delete()
            return Response(data={"result": message, 'ok': True}, status=status.HTTP_204_NO_CONTENT)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)


class RoomTypeViewSet(ViewSet):

    @swagger_auto_schema(
        operation_summary='Create Room Type',
        operation_description='Create Room Type',
        request_body=RoomTypeCreateSerializer,
        responses={201: 'Restaurant successfully created'},
        tags=['Restaurant']
    )
    def add_room_type(self, request):
        serializer = RoomTypeCreateSerializer(data=request.data)

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if serializer.is_valid():
            serializer.save()
            return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

        return Response(data={'result': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Show Room Type',
        operation_description='Show Room Type',
        responses={200: RoomTypeSerializer()},
        tags=['Restaurant']
    )
    def show_room_type(self, request):
        room_type = RoomType.objects.all()

        if room_type:
            serialize = RoomTypeSerializer(room_type, many=True, context={'request': request})
            return Response(data={'result': serialize.data, 'ok': True}, status=status.HTTP_200_OK)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

    @swagger_auto_schema(
        operation_summary='Edit Room Type',
        operation_description='Edit Restaurant Room Type',
        responses={200: RoomTypeSerializer(), 202: RoomTypeSerializer(), 400: 'Invalid request',
                   404: 'Room type does not exist'},
        tags=['Restaurant']
    )
    def edit_room_type(self, request, pk):
        room_type = RoomType.objects.filter(id=pk).first()
        serializer = RoomTypeSerializer(room_type, data=request.data, partial=True)

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if serializer.is_valid():
            serializer.save()
            return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_202_ACCEPTED)

        return Response(data={'result': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Delete Room Type',
        operation_description='Delete Room Type',
        responses={204: "Room type successfully deleted"},
        tags=['Restaurant']
    )
    def delete_room_type(self, request, pk):
        room_type = RoomType.objects.filter(id=pk).first()

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if room_type:
            message = f"{room_type} type was deleted"
            room_type.delete()
            return Response(data={"result": message, 'ok': True}, status=status.HTTP_204_NO_CONTENT)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)


class RestaurantRoomViewSet(ViewSet):

    @swagger_auto_schema(
        operation_summary='Create Room',
        operation_description='Create Restaurant Room',
        request_body=RoomCreateSerializer,
        responses={201: 'Restaurant room successfully created'},
        tags=['Restaurant']
    )
    def add_room(self, request):
        serializer = RoomCreateSerializer(data=request.data)

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if serializer.is_valid():
            serializer.save()
            return Response(data={"result": serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

        return Response(data={'result': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Show Restaurant',
        operation_description='Show Restaurant Info',
        responses={200: RoomSerializer()},
        tags=['Restaurant']
    )
    def show_restaurant_room(self, request, pk):
        room = RestaurantRoom.objects.filter(restaurant_id=pk)

        if room:
            room_serialize = RoomSerializer(room, many=True)
            return Response(data={'result': room_serialize.data, 'ok': True}, status=status.HTTP_200_OK)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

    @swagger_auto_schema(
        operation_summary='Show Room',
        operation_description='Show Restaurant Room detail Info',
        responses={200: RoomSerializer()},
        tags=['Restaurant']
    )
    def show_room_detail(self, request, pk):
        room = RestaurantRoom.objects.filter(restaurant_id=pk).first()

        if room:
            room_serialize = RoomSerializer(room, many=True)
            return Response(data={"result": room_serialize.data, 'ok': True}, status=status.HTTP_200_OK)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

    @swagger_auto_schema(
        operation_summary='Edit Room',
        operation_description='Edit Restaurant Room',
        responses={200: RoomSerializer(), 202: RoomSerializer(), 400: 'Invalid request',
                   404: 'Room type does not exist'},
        tags=['Restaurant']
    )
    def edit_room(self, request, pk):
        restaurant_room = RestaurantRoom.objects.filter(id=pk).first()
        serializer = RoomSerializer(restaurant_room, data=request.data, partial=True)

        if request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if serializer.is_valid():
            serializer.save()
            return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_202_ACCEPTED)

        return Response(data={'result': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Delete Room',
        operation_description='Delete Room',
        responses={204: "Room successfully deleted"},
        tags=['Restaurant']
    )
    def delete_room(self, request, pk):
        room = RestaurantRoom.objects.filter(id=pk).first()

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if room:
            message = f"{room} was deleted"
            room.delete()
            return Response(data={"result": message, 'ok': True}, status=status.HTTP_200_OK)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)


class MenuTypeViewSet(ViewSet):

    @swagger_auto_schema(
        operation_summary='Create Menu Type',
        operation_description='Create Restaurant Menu Type',
        request_body=MenuTypeCreateSerializer(),
        responses={201: 'Restaurant menu type successfully created', 400: 'Invalid request'},
        tags=['Restaurant']
    )
    def add_menu_type(self, request):
        serializer = MenuTypeCreateSerializer(data=request.data)

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if serializer.is_valid():
            serializer.save()
            return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

        return Response(data={'result': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Show Menu Type',
        operation_description='Show Restaurant menu type',
        responses={200: RoomSerializer()},
        tags=['Restaurant']
    )
    def show_menu_type(self, request):
        menu_type = MenuType.objects.all()

        if menu_type:
            serializer = MenuTypeSerializer(menu_type, many=True)
            return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

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

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if serializer.is_valid():
            serializer.save()
            return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_202_ACCEPTED)

        return Response(data={'result': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Delete Menu type',
        operation_description='Delete Menu type',
        responses={204: "Menu type successfully deleted"},
        tags=['Restaurant']
    )
    def delete_menu_type(self, request, pk):
        menu_type = MenuType.objects.filter(id=pk).first()

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if menu_type:
            message = f"{menu_type} type was deleted"
            menu_type.delete()
            return Response(data={'result': message, 'ok': True}, status=status.HTTP_204_NO_CONTENT)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)


class RestaurantMenuViewSet(ViewSet):

    # @swagger_auto_schema(
    #     operation_summary='Show Menu',
    #     operation_description='Show Restaurant menu',
    #     responses={200: MenuSerializer()},
    #     tags=['Restaurant']
    # )
    # def show_restaurant_menu(self, request):
    #     menu = RestaurantMenu.objects.filter(restaurant_id=request.data['restaurant_id'])
    #
    #     if menu:
    #         menu_serialize = MenuSerializer(menu, many=True)
    #         return Response(data={"result": menu_serialize.data, 'ok': True}, status=status.HTTP_200_OK)
    #
    #     raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

    @swagger_auto_schema(
        operation_summary='Create Menu',
        operation_description='Create Restaurant Menu',
        request_body=MenuSerializer(),
        responses={201: 'Restaurant menu successfully created'},
        tags=['Restaurant']
    )
    def add_restaurant_menu(self, request):
        serializer = MenuCreateSerializer(data=request.data)

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if serializer.is_valid():
            serializer.save()
            return Response(data={"result": serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

        return Response(data={"result": serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Show Menu detail',
        operation_description='Show Restaurant menu detail',
        responses={200: MenuSerializer()},
        tags=['Restaurant']
    )
    def show_menu_detail(self, request, pk):
        menu = RestaurantMenu.objects.filter(id=pk).first()

        if menu:
            serialize = MenuSerializer(menu, many=True)
            return Response(data={"result": serialize.data, 'ok': True}, status=status.HTTP_200_OK)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

    @swagger_auto_schema(
        operation_summary='Edit Menu',
        operation_description='Edit Restaurant Menu',
        responses={200: MenuSerializer(), 202: MenuSerializer(), 400: 'Invalid request',
                   404: 'Menu does not exist'},
        tags=['Restaurant']
    )
    def edit_menu(self, request, pk):
        restaurant_menu = RestaurantMenu.objects.filter(id=pk).first()
        serializer = MenuSerializer(restaurant_menu, data=request.data, partial=True)

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if serializer.is_valid():
            serializer.save()
            return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_202_ACCEPTED)

        return Response(data={'result': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Delete Menu',
        operation_description='Delete Menu',
        responses={204: "Menu successfully deleted"},
        tags=['Restaurant']
    )
    def delete_menu(self, request, pk):
        menu = RestaurantMenu.objects.filter(id=pk).first()

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if menu:
            message = f"{menu.name} is deleted"
            menu.delete()
            return Response(data={"result": message, 'ok': True}, status=status.HTTP_204_NO_CONTENT)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)


class CommentViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Show Comment list',
        operation_description='Show Restaurant Comment list',
        responses={200: CommentSerializer(), 400: 'Invalid request'},
        tags=['Restaurant']
    )
    def comment_list(self, request, pk):
        comments = Comment.objects.filter(restaurant_id=pk)

        if comments:
            serializer = CommentSerializer(comments, many=True)
            return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND.value)

    @swagger_auto_schema(
        operation_summary='Create Comment',
        operation_description='Create Restaurant Comment',
        request_body=CommentCreateSerializer(),
        responses={200: CommentSerializer(), 201: CommentSerializer(), 400: 'Invalid request'},
        tags=['Restaurant']
    )
    def comment_create(self, request):
        serializer = CommentCreateSerializer(data=request.data)

        if not request.user.is_authenticated:
            raise CustomApiException(error_code=ErrorCodes.UNAUTHORIZED.value)

        if serializer.is_valid():
            serializer.save()
            return Response(data={"result": serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

        return Response(data={'result': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantFilterViewSet(ViewSet):
    def filter_restaurant(self, reqeust):
        data = reqeust.GET
        query = data.get['query']
        restaurant = Restaurant.objects.filter(name__icontains=reqeust.name)

    @swagger_auto_schema(
        operation_summary='Show restaurants',
        operation_description='Show restaurants list',
        responses={200: RestaurantSerializer()},
        tags=['Restaurant']
    )
    def show_restaurant(self, request):
        restaurant_info = Restaurant.objects.all()
        if restaurant_info:
            restaurant_serialize = RestaurantSerializer(restaurant_info, many=True).data
            return Response(data={'result': restaurant_serialize}, status=status.HTTP_200_OK)
