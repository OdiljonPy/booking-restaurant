from django.contrib import admin
from .models import Manager


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'hire_date')
    list_filter = ['hire_date']

