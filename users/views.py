from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.decorators import login_required

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
            user = User.objects.get(username=username)
            return redirect('users:resetPass_1')

    return render(request, 'users/Forgot.html')

def resetP(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get('user')
        password1 = request.POST.get('pass1')
        password2 = request.POST.get('pass2')

        user_exist = User.objects.filter(username=username).exists()
        if(password1 != password2 or not user_exist):
            messages.warning(request, 'Password do not match or Wrong Username.')
            return redirect('users:resetPass')
        else:
            user = User.objects.get(username=username)
            user.set_password(password2)
            user.save()
            messages.success(request, 'Successfully change password for: ' + username + '.')
            return redirect('users:login')

    return render(request, 'users/Forgot_1.html')

def LogoutPage(request):
    logout(request)
    return redirect('users:login')

@login_required(login_url='users:login')
def View_Profile(request):
    return render(request, 'users/View_profile.html', {'user': request.user})