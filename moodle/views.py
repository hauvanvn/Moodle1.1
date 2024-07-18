from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import CourseClass as Class

@login_required(login_url="users:login")
def home(request):
    name = request.user.id
    courses = []
    notifications = []
    if Class.objects.exists():
        Class.objects.filter(users=name).order_by('date_create')
    return render(request, 'Home.html', {'courses' : courses, 'notifies' : notifications})