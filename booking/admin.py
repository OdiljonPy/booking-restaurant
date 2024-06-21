from django.contrib import admin
from .models import Occasion, OrderItems, OrderFreeTime, OrderFreeTable, Booking

admin.site.register(OrderItems)
admin.site.register(OrderFreeTime)
admin.site.register(OrderFreeTable)
admin.site.register(Booking)
admin.site.register(Occasion)