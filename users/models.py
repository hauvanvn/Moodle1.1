from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.dispatch import receiver
from django.conf import settings
from django.core.exceptions import ValidationError
# Create your models here.

def file_size(value):
    limit = 20 * 1024 * 1024 #MiB
    if value.size > limit:
        raise ValidationError('File too large. size should not exceed 20 MiB')

def upload_path_handle(instance, filename):
    return 'users/{id}/{file}'.format(id=instance.username, file=filename)

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
    avatar = models.ImageField(default='users/avatar.svg', upload_to=upload_path_handle, validators=[file_size])

# Delete old Avatar image
@receiver(models.signals.pre_save, sender=User)
def auto_delete_material(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_avatar = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False
    
    new_avatar = instance.avatar
    if not old_avatar == new_avatar and old_avatar.name != 'users/avatar.svg':
        if os.path.isfile(old_avatar.path):
            os.remove(old_avatar.path)
