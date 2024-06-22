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
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='GET',
        operation_description="Retrieve a list of all restaurants",
        responses={200: 'List of all restaurants'}
    )
    def list(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Retrieve a restaurant detail",
        responses={200: 'Restaurant detail', 404: 'Restaurant not found'}
    )
    def retrieve(self, request, rest_id):
        exists = Restaurant.objects.filter(pk=rest_id)
        if not exists.exists():
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(exists.first())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Show the total amount of payments made to the restaurant",
        responses={200: 'Restaurant balance'}
    )
    def balance(self, request, rest_id=None):
        payments = PaymentWithHistory.objects.filter(restaurants_id=rest_id)
        balance = payments.aggregate(total=Sum('amount')) or {'total': 0}
        balance['total'] = balance.get('total', 0)
        return Response(balance, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Show the full statistics of the restaurant from the start date to the end date",
        responses={200: 'Restaurant statistics', 400: 'Invalid date formats or Start date cannot be after the end date'}
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
        total_revenue = PaymentWithHistory.objects.filter(
            restaurants_id=rest_id, created_at__date__range=[parsed_start_date, parsed_end_date]
        ).aggregate(total=Sum('amount'))['total'] or 0

        stats = {
            'total_bookings': total_bookings,
            'total_revenue': total_revenue,
        }
        return Response(stats, status=status.HTTP_200_OK)


class BookingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all bookings of the restaurant",
        responses={200: 'List of all bookings'}
    )
    def list(self, request, rest_id):
        bookings = Booking.objects.filter(restaurants_id=rest_id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Retrieve info about booking status",
        responses={200: 'Booking detail', 400: 'Invalid date format', 404: 'Booking not found'}
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
        responses={404: 'Booking canceled or Booking not found'}
    )
    def cancel(self, request, rest_id, booking_id):
        booking_exists = Booking.objects.filter(pk=booking_id, restaurants_id=rest_id).first()
        if booking_exists is None:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        booking_exists.status = False
        booking_exists.save(update_fields=['status'])
        return Response({'status': 'Booking cancelled'}, status=status.HTTP_404_NOT_FOUND)


class ManagementViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new manager for the restaurant",
        responses={201: 'Manager Added Successfully', 400: 'Invalid data'}
    )
    def create(self, request, *args, **kwargs):
        manager_serializer = ManagerSerializer(data=request.data)
        if manager_serializer.is_valid():
            manager_serializer.save()
            return Response({"message": "Manager Added Successfully", "status": status.HTTP_201_CREATED})
        return Response({"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST})

    @swagger_auto_schema(
        operation_description="List the restaurants managers",
        responses={200: 'List of all managers'}
    )
    def list(self, request):
        managers = Manager.objects.all()
        serializer = ManagerSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployerViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new employee",
        responses={201: 'Employee added Successfully', 400: 'Invalid data'}
    )
    def create(self, request, *args, **kwargs):
        employer_serializer = EmployeeSerializer(data=request.data)
        if employer_serializer.is_valid():
            employer_serializer.save()
            return Response({"message": "Employee Added Successfully", "status": status.HTTP_201_CREATED})
        return Response({"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST})

    @swagger_auto_schema(
        operation_description="List the employees of a manager",
        responses={200: 'List of all Employees'}
    )
    def list(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
