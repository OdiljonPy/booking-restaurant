from django.urls import path
from .views import AdministratorViewSet, ManagementViewSet

urlpatterns = [
    path('restaurants/', ManagementViewSet.as_view({
        'get': 'list_restaurants',
    }), name='restaurant-list'),

    path('restaurants/<int:rest_id>/', ManagementViewSet.as_view({
        'get': 'retrieve_restaurant', 'delete': 'delete_restaurant'
    }), name='restaurant-detail'),

    path('restaurants/<int:rest_id>/balance/', ManagementViewSet.as_view({
        'get': 'restaurant_balance',
    }), name='restaurant-payment-balance'),

    path('restaurants/<int:rest_id>/statistics/', ManagementViewSet.as_view({
        'get': 'restaurant_statistics',
    }), name='restaurant-statistics'),
    path('restaurants/<int:rest_id>/bookings/', AdministratorViewSet.as_view({
        'get': 'booking_list', 'post': 'create_booking'
    }), name='restaurant-bookings'),

    path('restaurants/<int:rest_id>/bookings/<int:booking_id>/', AdministratorViewSet.as_view({
        'get': 'retrieve_booking', 'put': 'cancel_booking', 'delete': 'delete_booking'
    }), name='restaurant-bookings'),
    path('restaurants/<int:rest_id>/managers/admins/', ManagementViewSet.as_view({'post': 'create_admin'}))

]
