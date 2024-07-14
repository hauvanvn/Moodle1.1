from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CourseClass as Class

# Create your views here.
@login_required(login_url='users:login')
def view_class_list_All(request, slug):
    name = request.user.id
    courses = []
    if Class.objects.exists():
        Class.objects.filter(users=name).order_by('date_create')
    return render(request, 'Home.html', {'courses' : courses})