from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import CourseClass as Class, FileUpload, Notification
from users.models import User

# Create your views here.
@login_required(login_url='users:login')
def view_class_list(request, slug):
    name = request.user.id
    courses = []
    if Class.objects.exists():
        Class.objects.filter(users=name).order_by('date_create')
    return render(request, 'Hourse.html', {'courses' : courses})

@login_required(login_url='users:login')
def view_class_page(request, slug):
    course = Class.objects.get(slug=slug)
    files = FileUpload.objects.filter(inClass=course.id)
    return render(request, 'courses/Course.html', {'user': request.user, 'course' : course, 'files': files, 'slug': slug})

@login_required(login_url='users:login')
def view_participants(request, slug):
    course = Class.objects.get(slug=slug)
    users = User.objects.filter(id__in=course.participants.all()).order_by('-is_superuser', '-is_staff', 'username')
    page = Paginator(users, 20)

    page_number = request.GET.get("page")
    try:
        participants = page.page(page_number)
    except PageNotAnInteger:
        participants = page.page(1)
    except EmptyPage:
        participants = page.page(page.num_pages)

    return render(request, 'courses/Participants.html', {'user': request.user, 'participants': participants, 'course' : course})

@login_required(login_url='users:login')
def view_material(request, slug, filename):
    file = FileUpload.objects.get(name=filename)
    print(file.file.url)
    return render(request, 'courses/material_view.html', {'user': request.user,'file': file})

@login_required(login_url='users:login')
def view_announcement(reuqest, slug, id):
    notify = Notification.objects.get(id=id)

    if Notification.objects.exists():
        notifications = Notification.objects.filter(ForClass__participants__exact=reuqest.user.id)

    return render(reuqest, 'courses/View_annoucement.html', {'notify': notify, 'notifies' : notifications})

@login_required(login_url='users:login')
def view_post_announcement(request, slug):
    course = Class.objects.get(slug=slug)

    if request.method == "POST":
        title = request.POST.get('title')
        text = request.POST.get('description')

        notify = Notification(author=request.user, ForClass=course, title=title, text=text)
        notify.save()
        messages.success(request, 'Successfully post announcement!')
        return redirect('courses:class_page', slug=slug)

    if Notification.objects.exists():
        notifications = Notification.objects.filter(ForClass__participants__exact=request.user.id).order_by('date_created')

    return render(request, 'courses/Post_annoucement.html', {'notifies' : notifications})