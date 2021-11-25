from django.urls import path
from . import views

urlpatterns = [
    path('',views.orders,name='orders'),
    path('payments',views.payments,name='payments'),
    path('order_complete',views.order_complete,name='order_complete'),
]