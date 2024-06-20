from django.contrib import admin

from .models import Cards, PaymentWithHistory, OTP

admin.site.register(Cards)
admin.site.register(PaymentWithHistory)
admin.site.register(OTP)