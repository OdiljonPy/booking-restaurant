from drf_yasg.utils import swagger_auto_schema

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from authentication.models import User
from restaurants.models import RestaurantRoom, Restaurant
from booking.models import Booking, Occasion, Order

from booking.serializers import BookingSerializer, OccasionSerializer, PayingSerializer
from booking.dtos.requests import BookingRequestSerializer
from booking.dtos.responses import BookingResponseSerializer, OccasionResponseSerializer

from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_naive


class BookingViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create Booking',
        operation_description='Create a booking',
        request_body=BookingRequestSerializer,
        responses={201: BookingResponseSerializer()},
        tags=['Booking'],
    )
    def create_booking(self, request):
        data = request.data
        room = RestaurantRoom.objects.filter(id=request.data['room']).first()
        if not room:
            return Response(data={"error": "Room not found", "ok": False}, status=status.HTTP_400_BAD_REQUEST)

        if data['number_of_people'] > room.people_number:
            return Response(
                {"error": f"Number of people cannot be greater than the room number. Max:{room.people_number}",
                 'ok': False},
                status=status.HTTP_400_BAD_REQUEST)

        # Parse and make the datetimes naive
        planed_from = parse_datetime(data['planed_from'])
        planed_to = parse_datetime(data['planed_to'])
        if not (planed_from and planed_to and planed_to > planed_from):
            return Response({"error": "Invalid datetime format", "ok": False}, status=status.HTTP_400_BAD_REQUEST)
        planed_from = make_naive(planed_from)
        planed_to = make_naive(planed_to)

        bookings = Booking.objects.filter(
            room=room,
            planed_from__range=(planed_from, planed_to),
            planed_to__gte=planed_from,
            planed_from__lt=planed_to,

        )
        print(bookings.first())
        if bookings.exists():
            return Response({"error": "This room already booked", 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        data['restaurants'] = room.restaurant.id
        data['room'] = room.id
        data['author'] = User.objects.filter(id=request.data['author']).first().id
        # data['author'] = User.objects.filter(id=request.user.id).first().id

        # Update the data with naive datetimes
        data['planed_from'] = planed_from
        data['planed_to'] = planed_to

        booking_serializer = BookingSerializer(data=data)

        if booking_serializer.is_valid():
            booking_serializer.save()
            return Response(data={"data": booking_serializer.data, "message": "Booking Added Successfully",
                                  "status": status.HTTP_201_CREATED})
        else:
            print(booking_serializer.errors)
            return Response({"message": "Please fill the required details", "errors": booking_serializer.errors,
                             "status": status.HTTP_400_BAD_REQUEST})

    @swagger_auto_schema(
        operation_summary='Show bookings',
        operation_description='Show bookings list',
        responses={200: BookingResponseSerializer()},
        tags=['Booking']
    )
    def show_bookings(self, request, restaurant_pk):
        # user = request.user
        # restaurant = Restaurant.objects.filter(id=user.restaurant.id).first()
        restaurant = Restaurant.objects.filter(id=restaurant_pk).first()
        queryset = Booking.objects.filter(restaurants=restaurant)
        bookings = BookingResponseSerializer(queryset, many=True).data
        return Response(data={'bookings': bookings}, status=status.HTTP_200_OK)


class BookingActionsViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Show booking details',
        operation_description='Show booking details',
        responses={200: BookingSerializer()},
        tags=['Booking']
    )
    def detail_booking(self, request, pk):
        booking_detail = Booking.objects.filter(id=pk).first()
        booking_detail = BookingSerializer(booking_detail).data
        return Response(
            data={'data': booking_detail, 'message': f"{booking_detail['client_name']} {pk} id li buyurtmasi"},
            status=status.HTTP_200_OK)

    # @swagger_auto_schema(
    #     operation_summary='Pay booking',
    #     operation_description='Pay booking',
    #     responses={200: PayingSerializer()},
    #     tags=['Booking']
    # )
    def pay_booking(self, request, pk):
        booking_detail = Booking.objects.filter(id=pk).first()
        orders = Order.objects.filter()
        if booking_detail:
            data = PayingSerializer(data=booking_detail).data
            return Response(data={'data': data, 'message': f'{pk} id'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Cancelled booking',
        operation_description='Booking will be cancelled',
        responses={200: BookingSerializer()},
        tags=['Booking']
    )
    # TODO: Need to be optimize with set_status (url must be changed)
    def cancel_booking(self, request, pk):
        booking = Booking.objects.filter(id=pk).first()
        if not booking:
            return Response({"message": "Booking not found", "ok": False, "status": status.HTTP_400_BAD_REQUEST})
        serializer = BookingSerializer(booking, data={"status": "5"}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def set_status(self, request, pk):
        booking = Booking.objects.filter(id=pk).first()
        if not booking:
            return Response({"message": "Booking not found", "ok": False, "status": status.HTTP_400_BAD_REQUEST})
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Booking deleted',
        operation_description='Booking will be deleted',
        responses={204: BookingSerializer()},
        tags=['Booking']
    )
    def delete_booking(self, request, pk):
        booking_data = Booking.objects.filter(id=pk).first()
        if booking_data:
            booking_data.delete()
            return Response({"message": "Product delete Sucessfully", 'ok': True, "status": status.HTTP_204_NO_CONTENT})
        return Response(data={"message": "Product data not found", "ok": False}, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(ViewSet):
    def create_order(self, request):
        queryset = Order.objects.create(request.data)
        queryset.save()


class OccasionViewSet(ViewSet):

    @swagger_auto_schema(
        operation_summary='Create Occasion',
        operation_description='Occasion will be created',
        responses={201: OccasionResponseSerializer()},
        request_body=OccasionSerializer,
        tags=['Occasion']
    )
    def create_occasion(self, request):
        data = request.data
        queryset = OccasionSerializer(data=data)
        if queryset.is_valid():
            queryset.save()
        return Response(data={'data': queryset.data, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Occasions list',
        operation_description='Occasions list',
        responses={200: OccasionResponseSerializer()},
        tags=['Occasion']
    )
    def list_occasions(self, request):
        queryset = Occasion.objects.all()
        occasions = OccasionResponseSerializer(queryset, many=True).data
        return Response(data={'occasions': occasions, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Occasion data edit',
        operation_description='Occasion details will be updated',
        responses={202: OccasionResponseSerializer()},
        request_body=OccasionSerializer,
        tags=['Occasion']
    )
    def edit_occasion(self, request, pk):
        occasion = Occasion.objects.filter(id=pk).first()
        if not occasion:
            return Response(data={"error": "This occasion doesn't found", "ok": False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = OccasionResponseSerializer(occasion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"data": serializer.data, "message": "data changed", "ok": True},
                            status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Occasion deleted',
        operation_description='Occasion will be deleted',
        responses={204: "Occasion Deleted Successfully", 400: "This occasion doesn't found"},
        tags=['Occasion']
    )
    def delete(self, request, pk):
        occasion = Occasion.objects.filter(id=pk).first()
        if not occasion:
            return Response({"error": "This occasion doesn't found", "ok": False}, status=status.HTTP_400_BAD_REQUEST)
        occasion.delete()
        return Response(data={"message": "Deleted Successfully", 'ok': True, "status": status.HTTP_204_NO_CONTENT})


def calculate_free_times(room_id):
    room = RestaurantRoom.objects.filter(id=room_id).first()
    bookings = Booking.objects.filter(room=room)
    for i in bookings:
        print(i)
