from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
            return redirect('login')
        else:
            login(request, user)
            return redirect('home')

    return render(request, 'users/Login.html')

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
            return redirect('resetPass')
        else:
            user = User.objects.get(username=username)
            user.set_password(password2)
            user.save()
            messages.success(request, 'Successfully change password for: ' + username + '.')
            return redirect('login')

    return render(request, 'users/Forgot.html')

def LogoutPage(request):
    logout(request)
    return redirect("/")