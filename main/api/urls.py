from django.urls import path
from .views import OrderList

urlpatterns = [
    path('automated_orders', OrderList.as_view(), name='automated_orders'),
]
