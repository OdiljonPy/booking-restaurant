from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/management/', include('management.urls'))
]

"""
auth
restaurants - rating
menu/rooms - rating
booking - rooms with menu
payment - booking
telegram
management
# erp



urls

auth: /register, /otp/verify, /otp/resend, /login, /password/reset, /password/update, /me, /token/refresh
restaurant: /[post], /{id}[patch, put, delete], /filter[rating, location, price, popular, search], /{id}/menu, /{id}/rooms
booking: /[post], /my, /cancel[patch]
payment: /pay[post], /card/add|remove
telegram : /user/check, /user/add, rest/search, rest/filter, rest/menu, rest/rooms, ...
management: rest_id/booking[get, cancel], payment/balance, rest_id/statistics[fromDate, toDate]


"""
