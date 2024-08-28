from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import CourseClass as Class, Assignment
from .nav_infomation import getIn4

import datetime

@login_required(login_url="users:login")
def home(request):
    user, notifications, events = getIn4(request)
    courses = []
    assignment = {'title': 'No assignment', 'date_closed': '', 'ForClass': ''}

    if Class.objects.filter(participants=user.id).exists():
        courses_temp = Class.objects.filter(participants=user.id).order_by('-date_created')

        if Assignment.objects.filter(ForClass__in=courses_temp).exists():
            ev = [x for x in Assignment.objects.filter(ForClass__in=courses_temp).order_by('date_opened', 'date_opened') if not x.is_closed()]
            assignment = min(ev, key=lambda date: abs(date.date_closed - datetime.datetime.now(datetime.timezone.utc)))

        for course in courses_temp:
            teacher = course.participants.filter(is_staff=1)
            courses.append({'course': course, 'teacher': teacher})
    

    return render(request, 'View_home.html', {'user': user, 'notifies' : notifications, 'events': events, 
                                              'assignment' : assignment, 'courses' : courses})

def Http404NotFound(request):
    return render(request, '404.html')