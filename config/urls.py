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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

admin.site.site_header = 'Booking Admin'
admin.site.site_title = 'Booking Admin'
admin.site.index_title = 'Welcome to dashboard'

schema_view = get_schema_view(
    openapi.Info(
        title="MBG Store APIv1",
        default_version="v1",
        description="API for project MBG Store",
        terms_of_service="",
        contact=openapi.Contact(email="odiljonabduvaitov@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/restaurant/', include("restaurants.urls")),
    path('api/v1/booking/', include("booking.urls")),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view()),
    path('api/v1/token/refresh/', TokenRefreshView.as_view()),
    path('api/v1/token/verify/', TokenVerifyView.as_view()),
    path('api/v1/restaurant/', include("restaurants.urls")),

    re_path(r'static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    )
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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

auth: /register, /token/refresh, /otp/verify, /otp/resend, /login, /password/reset, /password/update, /me, 
restaurant: /[post], /{id}[patch, put, delete], /filter[rating, location, price, popular, search], /{id}/menu, /{id}/rooms
booking: /[post], /my, /cancel[patch]
payment: /pay[post], /card/add|remove
telegram : /user/check, /user/add, rest/search, rest/filter, rest/menu, rest/rooms, ...
management: rest_id/booking[get, cancel], payment/balance, rest_id/statistics[fromDate, toDate]


"""
