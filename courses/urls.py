"""
URL configuration for MyProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.view_class_list, name='class_list'),
    path('<slug:slug>', views.view_class_page, name='class_page'),
    path('<slug:slug>/participants', views.view_participants, name='participants'),
    path('<slug:slug>/annoucement/id=<int:id>', views.view_announcement, name='view_announcement'),
    path('<slug:slug>/annoucement/post', views.view_post_announcement, name='post_announcement'),
    path('<slug:slug>/<str:filename>', views.view_material, name='view_material'),  
]