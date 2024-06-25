from django.contrib import admin
from .models import Occasion, OrderItems, Booking

admin.site.register(OrderItems)
admin.site.register(Booking)
admin.site.register(Occasion)
