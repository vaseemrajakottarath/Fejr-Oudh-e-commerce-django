from django.urls import path
from . import views

urlpatterns = [
    path('signin',views.signin,name='signin'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('numberotp',views.numberotp,name='numberotp'),
    path('otp',views.otp,name='otp'),
    path('forgetpassword',views.forgetpassword,name='forgetpassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword',views.resetpassword,name='resetpassword'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('my_orders',views.my_orders,name='my_orders'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('change_password',views.change_password,name='change_password'),
    path('order_detail/<int:order_id>/',views.order_detail,name='order_detail'),
    path('address_management',views.address_management,name='address_management'),
    path('add_address',views.add_address,name='add_address'),
    path('edit_address/<int:id>/',views.edit_address,name='edit_address'),
    path('delete_address/<int:id>/',views.delete_address,name='delete_address')


]