from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.shortcuts import render

def user_login(request):
    return render(request, 'login.html')  # Template name should match


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate User
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            return redirect("dashboard")  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid username or password!")  # Show error message

    return render(request, "login.html")  # Render login page

# ✅ Fix: Define `dashboard_view`
def dashboard_view(request):
    return render(request, "dashboard.html")  # Render dashboard page


import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

# Temporary storage for OTPs
otp_storage = {}

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            otp_storage[email] = otp  # Store OTP temporarily
            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is: {otp}',
                'your-email@gmail.com',  # Replace with your Gmail
                [email],
                fail_silently=False,
            )
            request.session['reset_email'] = email  # Store email in session
            return redirect('otp_verification')
        except User.DoesNotExist:
            messages.error(request, "Email not found!")
    return render(request, 'password_reset_request.html')


def otp_verification(request):
    if request.method == "POST":
        email = request.session.get('reset_email')
        entered_otp = int(request.POST['otp'])

        if email in otp_storage and otp_storage[email] == entered_otp:
            return redirect('set_new_password')
        else:
            messages.error(request, "Invalid OTP!")
    return render(request, 'otp_verification.html')


from django.contrib.auth.hashers import make_password

def set_new_password(request):
    if request.method == "POST":
        email = request.session.get('reset_email')
        new_password = request.POST['password']
        
        if email:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password reset successful! Login again.")
            return redirect('login')

    return render(request, 'set_new_password.html')
