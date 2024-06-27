from drf_yasg.utils import swagger_auto_schema

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny

from authentication.models import User
from restaurants.models import RestaurantMenu, RestaurantRoom, Restaurant
from booking.models import Booking, Occasion, OrderItems
from booking.serializers import BookingSerializer, OccasionSerializer


class BookingViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create Booking',
        operation_description='Create a booking',
        request_body=BookingSerializer,
        responses={201: BookingSerializer()},
        tags=['Booking'],
    )
    def create_booking(self, request):
        data = request.data
        room = RestaurantRoom.objects.filter(id=request.data['room']).first()

        if not room:
            return Response({"message": "Room not found", "ok": False, "status": status.HTTP_400_BAD_REQUEST})

        data['restaurants'] = room.restaurant.id
        data['room'] = room.id
        data['author'] = User.objects.filter(id=request.data['author']).first().id
        # is_free = Booking.objects.filter(room=room.id, )
        booking_serializer = BookingSerializer(data=data)

        if booking_serializer.is_valid():
            booking_serializer.save()
            return Response({"message": "Booking Added Successfully", "status": status.HTTP_201_CREATED})
        else:
            print(booking_serializer.errors)
            return Response({"message": "Please fill the required details", "errors": booking_serializer.errors,
                             "status": status.HTTP_400_BAD_REQUEST})

    @swagger_auto_schema(
        operation_summary='Show bookings',
        operation_description='Show bookings list',
        responses={200: BookingSerializer()},
        tags=['Restaurant']
    )
    def show_bookings(self, request):
        queryset = Booking.objects.all()
        bookings = BookingSerializer(queryset, many=True).data
        return Response(data={'bookings': bookings}, status=status.HTTP_200_OK)


class BookingActionsViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Show booking details',
        operation_description='Show booking details',
        responses={200: BookingSerializer()},
        tags=['Restaurant']

    )
    def detail_booking(self, request, pk):
        booking_detail = Booking.objects.filter(id=pk).first()
        booking_detail = BookingSerializer(booking_detail).data
        return Response(
            data={'data': booking_detail, 'message': f'{booking_detail['client_name']} {pk} id li buyurtmasi'},
            status=status.HTTP_200_OK)

    def pay_booking(self, request, pk):
        booking_detail = Booking.objects.filter(id=pk).first()
        booking_pay = {}
        return Response(data={'data': booking_pay, 'message': f'{pk} id'}, )

    def cancel_booking(self, request, pk):
        pass

    def set_status(self, request, pk):
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


class OccasionActionsViewSet(ViewSet):
    def edit_occasion(self, request, pk):
        occasion = Occasion.objects.filter(id=pk).first()
        if occasion:
            occasion.name = request.data['occasion_name']
            occasion.save(update_fields=['occasion_name'])
            return Response(data={"message": f"{occasion} data was changed"}, status=status.HTTP_200_OK)
        return Response(data={"message": "Your data doesn't found"}, status=status.HTTP_400_BAD_REQUEST)


def calculate_free_times(room_id):
    room = RestaurantRoom.objects.filter(id=room_id).first()
