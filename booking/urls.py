from django.urls import path
from booking.views import BookingViewSet, BookingActionsViewSet, OccasionViewSet, OccasionActionsViewSet

urlpatterns = [
    path('', BookingViewSet.as_view({'get': 'show_bookings', 'post': 'create_booking'})),
    path('actions/<int:pk>',
         BookingActionsViewSet.as_view({'get': 'detail_booking', 'patch': 'set_status', 'delete': 'delete_booking'})),
    path('actions/cancel/<int:pk>', BookingActionsViewSet.as_view({'post': 'cancel_booking'})),
    path('actions/paying/<int:pk>', BookingActionsViewSet.as_view({'post': 'pay_booking'})),

    path('occasions/', OccasionViewSet.as_view({'get': '', 'post': ''})),
    path('occasions/actions/<int:pk>', OccasionActionsViewSet.as_view({'get': '', 'patch': '', 'delete': ''})),
]
