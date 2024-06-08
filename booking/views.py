from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny

from booking.models import Booking, Occasion
from booking.serializers import BookingSerializer, OccasionSerializer


class BookingViewSet(ViewSet):
    def create_booking(self, request, *args, **kwargs):
        booking_serializer = BookingSerializer(data=request.data)
        if booking_serializer.is_valid():
            booking_serializer.save()
            return Response({"message": "Booking Added Sucessfully", "status": status.HTTP_201_CREATED})
        return Response({"message": "please fill the datails", "status": status.HTTP_400_BAD_REQUEST})

    def show_bookings(self, request):
        queryset = Booking.objects.all()
        bookings = BookingSerializer(queryset, many=True).data
        return Response(data={'bookings': bookings}, )


class BookingActionsViewSet(ViewSet):
    def detail_booking(self, request, pk):
        booking_detail = Booking.objects.filter(id=pk).first()
        booking_serializer = BookingSerializer(booking_detail).data
        return Response(data={'data': booking_serializer.data, 'message': f'{pk} id li buyurtma'},
                        status=status.HTTP_200_OK)

    def pay_booking(self, request, *args, **kwargs):
        pass

    def cancel_booking(self, request, *args, **kwargs):
        pass

    def set_status(self, request, *args, **kwargs):
        pass

    def delete_booking(self, request, *args, **kwargs):
        booking_data = Booking.objects.filter(id=kwargs['pk'])
        if booking_data:
            booking_data.delete()
            return Response({"message": "Product delete Sucessfully", "status": status.HTTP_200_OK})
        return Response({"message": "Product data not found", "status": status.HTTP_400_BAD_REQUEST})


class OccasionViewSet(ViewSet):
    def create_occasion(self, request, *args, **kwargs):
        queryset = Occasion.objects.create(**request.data)
        queryset.save()
        return Response(data={'id': queryset.pk, 'message': 'your occasion has been created'}, )

    def list_occasions(self, request):
        queryset = Occasion.objects.all()
        occasions = OccasionSerializer(queryset, many=True).data
        return Response(data={'occasions': occasions}, )


class OccasionAcctionsViewSet(ViewSet):
    def edit_occasion(self, request, *args, **kwargs):
        occasion = Occasion.objects.get(pk=request.data['occasion'])


def free_tables_view(request):
    pass


def free_times_view(request):
    pass


def ordered_tables_view(request):
    pass


def ordered_times_view(request):
    pass
