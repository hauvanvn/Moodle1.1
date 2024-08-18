from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User, OtpToken
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .sendMail import sendOtp
from django.utils import timezone
from django.utils.timesince import timesince

from moodle.nav_infomation import getIn4
from courses.models import Notification
# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('pass')

        user = authenticate(request, username=username, password=password)
        if user is None or not user.is_active:
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
    user, notifications, events = getIn4(request)

    if request.method == "POST":
        if "reset_password" in request.POST:
            old_password = request.POST.get('old_pass')
            new_password = request.POST.get('new_pass')
            confirm_password = request.POST.get('con_pass')

            if user.check_password(old_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "Change password successful!")
                    return redirect('users:profile')
                else:
                    messages.warning(request, "New password not match to Verify password!")
                    return redirect('users:profile')
            else:
                messages.warning(request, "Your old password is not correct!")
                return redirect('users:profile')
        else:
            user.avatar = request.FILES['img']
            user.save()
            messages.success(request, "Change avatar successful!")
            return redirect('users:profile')

    return render(request, 'users/View_profile.html', {'user': user, 'notifies': notifications, 'events': events})

@login_required(login_url='users:login')
def view_all_announcements(request):
    user, notifications, events = getIn4(request)

    notifications = Notification.objects.filter(ForClass__participants__exact=user.id).order_by('-date_created')
    proccessed_notifications = []
    for notify in notifications:
        proccessed_notifications.append(notify.ForClass.className + ' - ' + notify.title)

        created_date = timezone.localtime(notify.date_created).strftime('%Y-%m-%d %H:%M:%S')
        print(notify.date_created)

        time_diff = timesince(notify.date_created)

        proccessed_notifications.append(time_diff + ' ago')
        proccessed_notifications.append(notify.author.avatar.url)
        proccessed_notifications.append(notify.title)
        proccessed_notifications.append('By ' + notify.author.first_name + notify.author.last_name + ' - ' + created_date)
        proccessed_notifications.append(notify.text)

    return render(request, 'users/View_all_anouncements.html', 
                  {'user': user, 'notifies': notifications, 'events': events, 'proccessed_notifications' : proccessed_notifications})