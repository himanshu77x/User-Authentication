from django.urls import path
from .views import user_login, password_reset_request, otp_verification, set_new_password, dashboard_view

urlpatterns = [
    path('', user_login, name='home'),  # Default home page -> login page
    path('login/', user_login, name='login'),
    path("dashboard/", dashboard_view, name="dashboard"), 
    path('password-reset/', password_reset_request, name='password_reset'),
    path('otp-verification/', otp_verification, name='otp_verification'),
    path('set-new-password/', set_new_password, name='set_new_password'),
]
