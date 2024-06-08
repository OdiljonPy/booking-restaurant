"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Ordering Rooms and Meals",
        default_version='v1', ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/restaurant/', include("restaurants.urls")),
    path('api/v1/booking/', include("booking.urls")),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

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
