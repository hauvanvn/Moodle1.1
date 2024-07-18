from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('getcode/', views.resetP_getCode, name="resetPass"),
    path('resetPass/', views.resetP, name="resetPass_1"),
    path('logout/', views.LogoutPage, name='logout')
]