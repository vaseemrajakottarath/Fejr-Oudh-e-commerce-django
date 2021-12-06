from django.urls import path
from . import views

urlpatterns = [
    path('',views.orders,name='orders'),
    path('payments',views.payments,name='payments'),
    path('user_orders',views.user_orders,name='user_orders'),
    path('order_details/<int:order_id>/',views.order_details,name='order_details'),
    path('cancel_order/<int:order_id>',views.cancel_order,name='cancel_order'),
    path('order_complete',views.order_complete,name='order_complete'),
    path('cash_on_delivery',views.cash_on_delivery,name='cash_on_delivery'),
    path('razorpay_payment_verification',views.razorpay_payment_verification,name='razorpay_payment_verification'),
    path('payment_failed',views.payment_failed,name='payment_failed')
]