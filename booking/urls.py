from django.urls import path
from booking.views import BookingViewSet, BookingActionsViewSet, OccasionViewSet, OccasionAcctionsViewSet, FreeOrderViewSet

urlpatterns = [
    path('', BookingViewSet.as_view({'get': 'show_bookings', 'post': 'create_booking'})),
    path('actions/<int:pk>',
         BookingActionsViewSet.as_view({'get': 'detail_booking', 'patch': 'set_status', 'delete': 'delete_booking'})),
    path('actions/cancel/<int:pk>', BookingActionsViewSet.as_view({'post': 'cancel_booking'})),
    path('actions/paying/<int:pk>', BookingActionsViewSet.as_view({'post': 'pay_booking'})),

    path('occasions/', OccasionViewSet.as_view({'get': '', 'post': ''})),
    path('occasions/actions/<int:pk>', OccasionAcctionsViewSet.as_view({'get': '', 'patch': '', 'delete': ''})),

    path('table/', FreeOrderViewSet.as_view({'post': 'add_free_table', 'get': 'add_free_table'})),
    path('order/<int:pk>', FreeOrderViewSet.as_view({'post': 'ordered_times_view'})),
    path('order_info/', FreeOrderViewSet.as_view({'get': 'ordered_times_view'}))
]
