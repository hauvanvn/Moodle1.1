from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import CourseClass as Class, Notification
from .nav_infomation import getIn4

@login_required(login_url="users:login")
def home(request):
    name = request.user.id
    courses = []
    notifications = []

    if Class.objects.exists():
        courses_temp = Class.objects.filter(participants=name).order_by('-date_created')
        for course in courses_temp:
            teacher = course.participants.filter(is_staff=1)
            courses.append({'course': course, 'teacher': teacher})

    
    user, notifications = getIn4(request)

    return render(request, 'View_home.html', {'user': user, 'courses' : courses, 'notifies' : notifications})