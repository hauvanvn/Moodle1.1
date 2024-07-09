from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('resetPass/', views.resetP, name="resetPass"),
    path('logout/', views.LogoutPage, name='logout')
]