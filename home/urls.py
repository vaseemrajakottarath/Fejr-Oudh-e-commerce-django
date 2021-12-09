from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('buy_now/<int:product_id>/',views.buy_now,name='buy_now')
    ]
#     path('signin',views.signin,name='signin'),
#     path('register',views.register,name='register')
# ]


