from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from restaurants.models import Restaurant
from booking.models import Booking
from .serializers import RestaurantSerializer, BookingSerializer
from payment.models import PaymentWithHistory


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    @action(detail=True, methods=['get'])
    def booking(self, request, pk=None):
        rest_id = pk
        booking_id = request.query_params.get('booking_id', None)
        date = request.query_params.get('date', None)
        bookings = Booking.objects.filter(restaurants_id=rest_id)
        if booking_id:
            bookings = bookings.filter(pk=booking_id)
        if date:
            bookings = bookings.filter(date=date)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def cancel_booking(self, request, pk=None):
        rest_id = pk
        booking_id = request.query_params.get('booking_id')
        try:
            booking = Booking.objects.get(pk=booking_id, restaurants_id=rest_id)
            booking.status = False
            booking.save()
            return Response({'status': 'Booking cancelled'}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def payment_balance(self, request, pk=None):
        rest_id = pk
        payments = PaymentWithHistory.objects.filter(restaurant_id=rest_id)
        balance = payments.aggregate(total=Sum('amount'))
        return Response(balance)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        rest_id = pk
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        bookings = Booking.objects.filter(restaurant_id=rest_id, date__range=[start_date, end_date])
        total_bookings = bookings.count()
        total_revenue = \
            PaymentWithHistory.objects.filter(restaurant_id=rest_id, date__range=[start_date, end_date]).aggregate(
                total=Sum('amount'))['total']
        stats = {
            'total_bookings': total_bookings,
            'total_revenue': total_revenue,
        }
        return Response(stats)
