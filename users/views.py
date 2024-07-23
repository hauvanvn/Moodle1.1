from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User, OtpToken
from django.contrib.auth.decorators import login_required

from .sendMail import sendOtp
from django.utils import timezone

from moodle.nav_infomation import getIn4
# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('pass')

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.warning(request, 'Username or Password is incorrect.')
            return redirect('users:login')
        else:
            login(request, user)
            return redirect('home')

    return render(request, 'users/Login.html')

def resetP_getCode(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST.get('user')

        user_exist = User.objects.filter(username=username).exists()
        if (not user_exist):
            messages.warning(request, 'Wrong Username.')
            return redirect('users:resetPass')
        else:
            request.session['username'] = username
            user = User.objects.get(username=username)
            sendOtp(user)
            return redirect('users:resetPass_1')

    return render(request, 'users/Forgot.html')

def resetP(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.session['username']
        password1 = request.POST.get('pass1')
        password2 = request.POST.get('pass2')
        code = request.POST.get('code')

        user = User.objects.get(username=username)
        otp = OtpToken.objects.filter(user=user).last()
        
        if otp.otp_expired_at > timezone.now():
            if(password1 != password2):
                messages.warning(request, 'Password do not match.')
                return redirect('users:resetPass_1')
            elif code != otp.otp_code:
                messages.warning(request, 'Wrong otp.')
                return redirect('users:resetPass_1')
            else:
                user.set_password(password2)
                user.save()
                messages.success(request, 'Successfully change password for: ' + username + '.')
                return redirect('users:login')
        else:
            messages.warning(request, 'OTP has expired.')
            return redirect('users:resetPass')

    return render(request, 'users/Forgot_1.html')

def LogoutPage(request):
    logout(request)
    return redirect('users:login')

@login_required(login_url='users:login')
def View_Profile(request):
    user, notifications = getIn4(request)
    return render(request, 'users/View_profile.html', {'user': user, 'notifies': notifications})