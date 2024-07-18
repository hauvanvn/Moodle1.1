from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        NONE = "NONE", "None"

    inClass = models.CharField(max_length=8, null=True, blank=True)
    birthday = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=6, choices=Gender, default=Gender.NONE)
    country = models.CharField(max_length=100, default="Viet Nam")
    city = models.CharField(max_length=100, default="Ho Chi Minh City")
    avatar = models.ImageField(null=True, blank=True, upload_to='users/image')
