from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django.db.models import Sum

from booking.dtos.requests import BookingRequestSerializer
from restaurants.models import Restaurant
from booking.models import Booking
from restaurants.serializers import RestaurantSerializer
from booking.serializers import BookingSerializer
from .models import Administrator
from .serializers import DateRangeQuerySerializer, \
    DateQuerySerializer, AdministratorSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager, IsManagerOrAdministrator
from drf_yasg import openapi


class ManagementViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Retrieve a restaurant detail",
        operation_summary="Get restaurant details",
        responses={
            200: openapi.Response(
                description='Restaurant detail',
            ),
            404: openapi.Response(
                description='Restaurant not found',
            )
        },
    )
    @permission_classes([IsAuthenticated, IsManager])
    def retrieve_restaurant(self, request, rest_id):
        exists = Restaurant.objects.filter(pk=rest_id)
        if not exists.exists():
            return Response(data={'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(exists.first())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Show the balance of a restaurant",
        operation_summary="Retrieve restaurant balance",
        responses={
            200: openapi.Response(
                description="Restaurant balance",
            ),
            404: openapi.Response(
                description="Restaurant not found",
            ),
        },
    )
    @permission_classes([IsAuthenticated, IsManager])
    def restaurant_balance(self, request, rest_id):
        restaurant_exists = Restaurant.objects.filter(pk=rest_id)
        if not restaurant_exists.exists():
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        restaurant = restaurant_exists.first()
        return Response(data={f'id: {restaurant.id},name:{restaurant.name},total balance: {restaurant.balance}'},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get statistics of bookings based on date range",
        operation_summary="Get booking statistics based on date range",
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Start date in YYYY-MM-DD format",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="End date in YYYY-MM-DD format",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description='Booking statistics',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_bookings': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_revenue': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT)
                    }
                )
            ),
            400: openapi.Response(
                description='Invalid date format or date range'
            )
        },
    )
    @permission_classes([IsAuthenticated, IsManager])
    def restaurant_statistics(self, request, rest_id):
        restaurant = Restaurant.objects.filter(id=rest_id)
        if not restaurant.exists():
            return Response(data={'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        query_serializer = DateRangeQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        parsed_start_date = query_serializer.validated_data['start_date']
        parsed_end_date = query_serializer.validated_data['end_date']
        bookings = Booking.objects.filter(restaurants_id=rest_id,
                                          booked_time__date__range=[parsed_start_date, parsed_end_date])
        total_bookings = bookings.count()
        total_revenue = bookings.aggregate(total=Sum('total_sum'))['total'] or 0

        stats = {
            'restaurant_id': rest_id,
            'restaurant_name': restaurant.first().name,
            'total_bookings': total_bookings,
            'total_revenue': total_revenue,
        }
        return Response(data={stats}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete the restaurant",
        operation_summary="Delete restaurant",
        responses={
            204: openapi.Response(
                description='Restaurant deleted successfully',
            ),
            404: openapi.Response(
                description='Restaurant not found',
            ),
        },
    )
    @permission_classes([IsAuthenticated, IsManager])
    def delete_restaurant(self, request, rest_id):
        restaurant_exists = Restaurant.objects.filter(pk=rest_id)
        if not restaurant_exists.exists():
            return Response('Restaurant not found', status=status.HTTP_404_NOT_FOUND)
        restaurant = restaurant_exists.first()
        restaurant.delete()
        return Response(data={"message": 'Restaurant deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Create a new admin",
        operation_summary="Add an admin",
        request_body=AdministratorSerializer,
        responses={
            201: openapi.Response(
                description='Administrator Added Successfully',
            ),
            400: openapi.Response(
                description='Invalid data',
            )
        },
    )
    @permission_classes([IsAuthenticated, IsManager])
    def create_admin(self, request):
        administrator_serializer = AdministratorSerializer(data=request.data)
        if administrator_serializer.is_valid():
            administrator_serializer.save()
            return Response(data={"message": "Administrator Added Successfully", "status": status.HTTP_201_CREATED})
        return Response(data={"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="List all employees",
        operation_summary="Get all employees",
        responses={
            200: openapi.Response(
                description='List of all employees',
            )
        },
    )
    @permission_classes([IsAuthenticated, IsManager])
    def list_admins(self, request):
        administrator = Administrator.objects.all()
        serializer = AdministratorSerializer(administrator, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete the admin",
        operation_summary="Delete admin",
        responses={
            204: openapi.Response(
                description='Admin deleted Successfully',
            ),
            404: openapi.Response(
                description='Admin not found'
            )
        },
    )
    @permission_classes([IsAuthenticated, IsManager])
    def delete_admin(self, request, rest_id, admin_id):
        admin_exists = Administrator.objects.filter(pk=admin_id, managager__restaurant_id=rest_id).exists()
        if not admin_exists.exists():
            return Response(data={'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin_exists.first().delete()
        return Response(data={'message': 'Admin deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Create booking",
        operation_summary="Add booking",
        request_body=BookingRequestSerializer,
        responses={
            201: openapi.Response(
                description='Booking Added Successfully',
            ),
            400: openapi.Response(
                description='Please fill the details correctly',
            )
        },
    )
    @permission_classes([IsAuthenticated, IsManagerOrAdministrator])
    def create_booking(self, request):
        booking_serializer = BookingSerializer(data=request.data)
        if booking_serializer.is_valid():
            booking_serializer.save()
            return Response(data={"message": "Booking Added Successfully"}, status=status.HTTP_201_CREATED)
        return Response(data={"message": "Please fill the details correctly"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="List bookings based on date",
        operation_summary="Get all bookings based on date",
        manual_parameters=[
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Date in YYYY-MM-DD format",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description='List of all bookings',
                schema=BookingSerializer(many=True)
            ),
            400: openapi.Response(
                description='"Date has wrong format. Use one of these formats instead: YYYY-MM-DD."'
            )
        },
    )
    @permission_classes([IsAuthenticated, IsManagerOrAdministrator])
    def booking_list(self, request, rest_id):
        query_serializer = DateQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        parsed_date = query_serializer.validated_data['date']
        bookings = Booking.objects.filter(restaurants_id=rest_id, booked_time__date=parsed_date)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Retrieve a booking detail",
        operation_summary="Get booking details",
        responses={
            200: openapi.Response(
                description='Booking detail',
            ),
            404: openapi.Response(
                description='Booking not found',
            ),
        },
    )
    @permission_classes([IsAuthenticated, IsManagerOrAdministrator])
    def retrieve_booking(self, request, rest_id, booking_id):
        booking_exists = Booking.objects.filter(pk=booking_id, restaurants_id=rest_id)
        if not booking_exists.exists():
            return Response(data={'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        bookings = booking_exists
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Cancel the booking",
        operation_summary="Cancel booking",
        responses={
            200: openapi.Response(
                description='Booking cancelled',
            ),
            404: openapi.Response(
                description='Booking not found',
            )
        },
    )
    @permission_classes([IsAuthenticated, IsManagerOrAdministrator])
    def cancel_booking(self, request, rest_id, booking_id):
        booking_exists = Booking.objects.filter(pk=booking_id, restaurants_id=rest_id)
        if not booking_exists.exists():
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        booking = booking_exists.first()
        booking.status = 5
        booking.save(update_fields=['status'])
        return Response(data={'status': 'Booking cancelled'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete the booking",
        operation_summary="Delete booking",
        responses={
            204: openapi.Response(
                description='Booking deleted Successfully',
            ),
            404: openapi.Response(
                description='Restaurant or Booking not found'
            )
        },
    )
    @permission_classes([IsAuthenticated, IsManager])
    def delete_booking(self, request, rest_id, booking_id):
        restaurant = Restaurant.objects.filter(pk=rest_id)
        if not restaurant.exists():
            return Response(data={'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        booking_exists = Booking.objects.filter(pk=booking_id, restaurants_id=rest_id)
        if not booking_exists.exists():
            return Response(data={'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        booking_exists.first().delete()
        return Response(data={'message': 'Booking deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
