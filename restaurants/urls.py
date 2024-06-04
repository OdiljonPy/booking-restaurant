from django.urls import path
from .views import restaurant_filter_view

urlpatterns = [
    path('', restaurant_filter_view, name='restaurant_filter'),

    path('add/restauran/', ),
    path('add/room/', ),
    path('add/menu/', ),

    path('add/restaurant/category', ),
    path('add/room/type', ),

    path('actions/restaurant', ),
    path('actions/room', ),
    path('actions/menu', ),

]
