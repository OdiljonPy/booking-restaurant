from django.contrib import admin

from authentication.models import User, OTP

admin.site.register(User)
admin.site.register(OTP)