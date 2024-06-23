from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils.dateparse import parse_date
from restaurants.models import Restaurant
from booking.models import Booking
from .models import Role, Manager, Employee, PerformanceReview, Project, Task, LeaveRequest
from .serializers import RestaurantSerializer, BookingSerializer, ManagerSerializer, EmployeeSerializer
from payment.models import PaymentWithHistory
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi


class RestaurantViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all restaurants",
        operation_summary="Get all restaurants",
        responses={
            200: openapi.Response(
                description='List of all restaurants',
                examples={
                    'application/json': [
                        {"id": 1, "name": "Restaurant 1"},
                        {"id": 2, "name": "Restaurant 2"}
                    ]
                }
            )
        },
    )
    def list(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Retrieve a restaurant detail",
        operation_summary="Get restaurant details",
        responses={
            200: openapi.Response(
                description='Restaurant detail',
                examples={
                    'application/json': {
                        "id": 1,
                        "author": "Author Name",
                        "name": "Restaurant Name",
                        "description": "Restaurant Description",
                        "picture": "http://example.com/picture.jpg",
                        "service_fee": 10.5,
                        "balance": 1000.0,
                        "booking_count_total": 25,
                        "booking_count_day_by_day": 5,
                        "address": "Olmazor distrit,BA IT Academy,Tashkent",
                        "phone": "+123456789",
                        "email": "restaurant@example.com",
                        "category": "Category Name"
                    }
                }
            ),
            404: openapi.Response(
                description='Restaurant not found',
                examples={
                    'application/json': {"error": "Restaurant not found"}
                }
            )
        },
    )
    def retrieve(self, request, rest_id):
        exists = Restaurant.objects.filter(pk=rest_id)
        if not exists.exists():
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(exists.first())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Show the balance of a restaurant",
        operation_summary="Retrieve restaurant balance",
        responses={
            200: openapi.Response(
                description="Restaurant balance",
                examples={
                    "application/json": {
                        "total balance": 1234.56
                    }
                }
            ),
            404: openapi.Response(
                description="Restaurant not found",
                examples={
                    "application/json": {
                        "error": "Restaurant not found"
                    }
                }
            ),
        },
    )
    def balance(self, request, rest_id):
        restaurant = Restaurant.objects.filter(pk=rest_id).first()
        balance = restaurant.balance
        return Response({f'total balance: {balance}'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Show the full statistics of the restaurant from the start date to the end date",
        operation_summary="Retrieve restaurant statistics",
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
                description="Restaurant statistics",
                examples={
                    "application/json": {
                        "total_bookings": 50,
                        "total_revenue": 10000.00
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid date formats or Start date cannot be after the end date",
                examples={
                    "application/json": {
                        "error": "Invalid start date format"
                    },
                    "application/json": {
                        "error": "Invalid end date format"
                    },
                    "application/json": {
                        "error": "Start date cannot be after end date"
                    }
                }
            ),
        },
    )
    def statistics(self, request, rest_id):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        parsed_start_date = parse_date(start_date)
        parsed_end_date = parse_date(end_date)
        if not start_date or not parsed_start_date:
            return Response({'error': 'Invalid start date format'}, status=status.HTTP_400_BAD_REQUEST)

        if not end_date or not parsed_end_date:
            return Response({'error': 'Invalid end date format'}, status=status.HTTP_400_BAD_REQUEST)

        if parse_date(start_date) > parse_date(end_date):
            return Response({'error': 'Start date cannot be after end date'}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(restaurants_id=rest_id,
                                          booked_time__date__range=[parsed_start_date, parsed_end_date])
        total_bookings = bookings.count()
        total_revenue = bookings.aggregate(
            total=Sum('total_sum'))['total'] or 0
        stats = {
            'total_bookings': total_bookings,
            'total_revenue': total_revenue,
        }
        return Response(stats, status=status.HTTP_200_OK)


class BookingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all bookings of the restaurant",
        operation_summary="Get all bookings",
        responses={
            200: openapi.Response(
                description='List of all bookings',
                examples={
                    'application/json': [
                        {"id": 1, "restaurant_id": 1, "booked_time": "2024-06-23T10:00:00Z", "status": True},
                        {"id": 2, "restaurant_id": 1, "booked_time": "2024-06-24T10:00:00Z", "status": False}
                    ]
                }
            )
        },
    )
    def list(self, request, rest_id):
        bookings = Booking.objects.filter(restaurants_id=rest_id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Retrieve info about booking status",
        operation_summary="Get booking details",
        manual_parameters=[
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Date in YYYY-MM-DD format",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                description='Booking detail',
                examples={
                    'application/json': [
                        {"id": 1, "restaurant_id": 1, "booked_time": "2024-06-23T10:00:00Z", "status": True}
                    ]
                }
            ),
            400: openapi.Response(
                description='Invalid date format',
                examples={
                    'application/json': {"error": "Invalid date format"}
                }
            ),
            404: openapi.Response(
                description='Booking not found',
                examples={
                    'application/json': {"error": "Booking not found"}
                }
            ),
        },
    )
    def retrieve(self, request, rest_id, booking_id):
        date = request.query_params.get('date')
        booking_exists = Booking.objects.filter(pk=booking_id, restaurants_id=rest_id)
        if not booking_exists.exists():
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        bookings = booking_exists
        if date and not parse_date(date):
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
        if date:
            bookings = Booking.objects.filter(booked_time__date=date)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Cancel the booking",
        operation_summary="Cancel booking",
        responses={
            200: openapi.Response(
                description='Booking cancelled',
                examples={
                    'application/json': {"status": "Booking cancelled"}
                }
            ),
            404: openapi.Response(
                description='Booking not found',
                examples={
                    'application/json': {"error": "Booking not found"}
                }
            )
        },
    )
    def cancel(self, request, rest_id, booking_id):
        booking_exists = Booking.objects.filter(pk=booking_id, restaurant_id=rest_id).first()
        if booking_exists is None:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        booking_exists.status = False
        booking_exists.save(update_fields=['status'])
        return Response({'status': 'Booking cancelled'}, status=status.HTTP_200_OK)


class ManagementViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new manager for the restaurant",
        operation_summary="Add a manager",
        request_body=ManagerSerializer,
        responses={
            201: openapi.Response(
                description='Manager Added Successfully',
                examples={
                    'application/json': {"message": "Manager Added Successfully", "status": status.HTTP_201_CREATED}
                }
            ),
            400: openapi.Response(
                description='Invalid data',
                examples={
                    'application/json': {"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST}
                }
            )
        },
    )
    def create(self, request, *args, **kwargs):
        manager_serializer = ManagerSerializer(data=request.data)
        if manager_serializer.is_valid():
            manager_serializer.save()
            return Response({"message": "Manager Added Successfully", "status": status.HTTP_201_CREATED})
        return Response({"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST})

    @swagger_auto_schema(
        operation_description="List all restaurant managers",
        operation_summary="Get all managers",
        responses={
            200: openapi.Response(
                description='List of all managers',
                examples={
                    'application/json': [
                        {"id": 1, "name": "Manager 1"},
                        {"id": 2, "name": "Manager 2"}
                    ]
                }
            )
        },
    )
    def list(self, request):
        managers = Manager.objects.all()
        serializer = ManagerSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployerViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new employee",
        operation_summary="Add an employee",
        request_body=EmployeeSerializer,
        responses={
            201: openapi.Response(
                description='Employee added Successfully',
                examples={
                    'application/json': {"message": "Employee Added Successfully", "status": status.HTTP_201_CREATED}
                }
            ),
            400: openapi.Response(
                description='Invalid data',
                examples={
                    'application/json': {"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST}
                }
            )
        },
    )
    def create(self, request, *args, **kwargs):
        employer_serializer = EmployeeSerializer(data=request.data)
        if employer_serializer.is_valid():
            employer_serializer.save()
            return Response({"message": "Employee Added Successfully", "status": status.HTTP_201_CREATED})
        return Response({"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST})

    @swagger_auto_schema(
        operation_description="List the employees of a manager",
        operation_summary="Get all employees",
        responses={
            200: openapi.Response(
                description='List of all employees',
                examples={
                    'application/json': [
                        {"id": 1, "name": "Employee 1"},
                        {"id": 2, "name": "Employee 2"}
                    ]
                }
            )
        },
    )
    def list(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
