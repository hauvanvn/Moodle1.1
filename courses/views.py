from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import CourseClass as Class, FileUpload, Notification, Comment
from .forms import FileUploadForm, AnnouncementForm
from users.models import User

from moodle.nav_infomation import getIn4

import datetime

# Create your views here.
@login_required(login_url='users:login')
def view_class_list(request):
    user, notifications = getIn4(request)

    courses = []

    if Class.objects.exists():
        cur_date = datetime.date.today()
        open_date = datetime.date(cur_date.year - 3, cur_date.month, cur_date.day)

        courses = Class.objects.filter(participants=user.id).order_by('-date_created')

    return render(request, 'courses/View_courses_list.html', {'user': user, 'notifies': notifications, 'courses': courses})

@login_required(login_url='users:login')
def view_class_page(request, slug):
    course = Class.objects.get(slug=slug)
    files = FileUpload.objects.filter(inClass=course.id)

    user, notifications = getIn4(request)
    
    if request.method == "POST":
        if 'delete_material' in request.POST:
            # Delete material
            file_delete = FileUpload.objects.get(id=request.POST.get('delete_material'))
            file_delete.delete()
            messages.success(request, "Delete successful!")
            return redirect('courses:class_page', slug=slug)
        else:
            # Add material
            name = request.POST.get('name')
            if 'General' in request.POST:
                group = FileUpload.FileGroup.GENERAL
            else:
                group = FileUpload.FileGroup.LECTURE

            type = FileUpload.FileType.FILE
            link = request.POST.get('link')
            if link == '':
                type = FileUpload.FileType.FILE
            else:
                type = FileUpload.FileType.LINK

            # Check input all infomations
            if name == '':
                messages.warning(request, "Missing name of material!")
                return redirect('courses:class_page', slug=slug)
            if type == FileUpload.FileType.FILE:
                if request.FILES is None:
                    messages.warning(request, "Missing file upload!")
                    return redirect('courses:class_page', slug=slug)
            else:
                if link == '':
                    messages.warning(request, "Missing link!")
                    return redirect('courses:class_page', slug=slug)

            form = FileUploadForm({'name': name, 'group': group, 'type': type, 'link': link, 'inClass': course}, request.FILES)
            
            if form.is_valid():
                form.save()
                messages.success(request, "Upload " + name + "successful!")
                return redirect('courses:class_page', slug=slug)
            else:
                return render(request, 'courses/View_course_teacher.html', 
                        {'user': user, 'notifies': notifications, 'course' : course, 'files': files, 'form': form})
        
    # Teacher view
    if user.is_staff and not user.is_superuser:
        return render(request, 'courses/View_course_teacher.html', 
                  {'user': user, 'notifies': notifications, 'course' : course, 'files': files, 'form': FileUploadForm()})
    else:
    # Student view
        return render(request, 'courses/View_course.html', 
                    {'user': user, 'notifies': notifications, 'course' : course, 'files': files})

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

    user, notifications = getIn4(request)

    return render(request, 'courses/View_participants.html', {'user': user, 'notifies': notifications, 'participants': participants, 'course' : course})

@login_required(login_url='users:login')
def view_material(request, slug, filename):
    file = FileUpload.objects.get(name=filename)
    user, notifications = getIn4(request)

    comments = Comment.objects.filter(file=file).order_by('-date_created')

    return render(request, 'courses/View_material.html', 
                  {'user': user, 'notifies': notifications,'file': file, 'comments': comments})

@login_required(login_url='users:login')
def view_announcement(request, slug, id):
    notify = Notification.objects.get(id=id)

    user, notifications = getIn4(request)

    return render(request, 'courses/View_annoucement.html', {'user': user, 'notifies': notifications, 'notify': notify})

@login_required(login_url='users:login')
def view_post_announcement(request, slug):
    course = Class.objects.get(slug=slug)
    user, notifications = getIn4(request)

    if request.method == "POST":
        title = request.POST.get('title')
        text = request.POST.get('text')
        form = AnnouncementForm({'title' : title, 'text' : text, 'author' : user, 'ForClass' : course})
        if form.is_valid:
            form.save()
            messages.success(request, 'Successfully post announcement!')
            return redirect('courses:class_page', slug=slug)
        else:
            return render(request, 'courses/Post_annoucement.html', {'user': user, 'notifies': notifications, 'form': form})

    return render(request, 'courses/Post_annoucement.html', {'user': user, 'notifies': notifications, 'form': AnnouncementForm()})