from django.contrib import admin

from .models import Card, PaymentWithHistory, OTP

admin.site.register(Card)
admin.site.register(PaymentWithHistory)
admin.site.register(OTP)