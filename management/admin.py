from django.contrib import admin
from .models import Manager, BookingCustomer


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'hire_date')
    list_filter = ['hire_date']


@admin.register(BookingCustomer)
class BookingCustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number')
