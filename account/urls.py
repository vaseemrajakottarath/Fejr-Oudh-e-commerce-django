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
    path('dashboard',views.dashboard,name='dashboard')

]