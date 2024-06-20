from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils.dateparse import parse_date
from restaurants.models import Restaurant
from booking.models import Booking
from .serializers import RestaurantSerializer, BookingSerializer
from payment.models import PaymentWithHistory


class RestaurantViewSet(viewsets.ViewSet):
    # queryset = Restaurant.objects.all()
    # serializer_class = RestaurantSerializer

    def list(self, request):
        queryset = Restaurant.objects.all()
        serializer = RestaurantSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        if not Restaurant.objects.filter(pk=pk).exists():
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

        restaurant = Restaurant.objects.get(pk=pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=True, methods=['get'], url_path='bookings')
    def booking(self, request, pk=None):
        booking_id = request.query_params.get('booking_id')
        date = request.query_params.get('date')

        if booking_id and not booking_id.isdigit():
            return Response({'error': 'Invalid booking ID'}, status=status.HTTP_400_BAD_REQUEST)

        if date and not parse_date(date):
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(restaurants_id=pk)
        if booking_id:
            bookings = bookings.filter(pk=booking_id)
        if date:
            bookings = Booking.objects.filter(booked_time__date=date)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=True, methods=['delete'], url_path='cancel-booking')
    def cancel_booking(self, request, pk=None):
        booking_id = request.query_params.get('booking_id')

        if not booking_id or not booking_id.isdigit():
            return Response({'error': 'Invalid booking ID'}, status=status.HTTP_400_BAD_REQUEST)

        if not Booking.objects.filter(pk=booking_id, restaurants_id=pk).exists():
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        booking = Booking.objects.get(pk=booking_id, restaurants_id=pk)
        booking.status = False
        booking.save()
        return Response({'status': 'Booking cancelled'}, status=status.HTTP_404_NOT_FOUND)

    # @action(detail=True, methods=['get'], url_path='payment-balance')
    def payment_balance(self, request, pk=None):
        payments = PaymentWithHistory.objects.filter(restaurants_id=pk)
        balance = payments.aggregate(total=Sum('amount')) or {'total': 0}
        balance['total'] = balance.get('total', 0)
        return Response(balance, status=status.HTTP_200_OK)

    # @action(detail=True, methods=['get'], url_path='statistics')
    def statistics(self, request, pk=None):
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

        bookings = Booking.objects.filter(restaurants_id=pk,
                                          booked_time__date__range=[parsed_start_date, parsed_end_date])
        total_bookings = bookings.count()
        total_revenue = PaymentWithHistory.objects.filter(
            restaurants_id=pk, created_at__date__range=[parsed_start_date, parsed_end_date]
        ).aggregate(total=Sum('amount'))['total'] or 0

        stats = {
            'total_bookings': total_bookings,
            'total_revenue': total_revenue,
        }
        return Response(stats, status=status.HTTP_200_OK)
