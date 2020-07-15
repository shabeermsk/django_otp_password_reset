from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name ='accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', views.HomeView.as_view(), name='home'),
    path('send_otp/', views.send_otp, name='sendotp'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('change_password/', views.user_change_password_view, name='new_password'),
]
