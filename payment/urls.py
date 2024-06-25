from django.urls import path

from .views import PaymeCallBackAPIView, OrderStatusApiView

urlpatterns = [

    path("merchant/", PaymeCallBackAPIView.as_view()),
    path("create-order/", OrderStatusApiView.as_view())

]
