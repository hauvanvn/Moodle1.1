from django.db import models
from users.models import User, file_size
import os
from django.dispatch import receiver
from django.utils import timezone
from django.utils.timesince import timesince
import datetime

# Create your models here.
class Course(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    date_created = models.DateField()

    def __str__(self):
        return self.id + ' - ' + self.name

class CourseClass(models.Model):
    id = models.BigAutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    className = models.CharField(max_length=10)
    participants = models.ManyToManyField(User, blank=True)

    date_created = models.DateField(auto_now_add=True)
    date_end = models.DateField(blank=True, null=True)
    slug = models.SlugField()

    def is_course_end(self):
        return self.date_end < datetime.date.today()

    def __str__(self):
        return str(self.course) + '_' + self.className

def upload_file_path_handle(instance, filename):
    return 'courses/{id}/{file}'.format(id=instance.inClass.id, file=filename)

class FileUpload(models.Model):
    class FileGroup(models.TextChoices):
        GENERAL = "GENERAL", "General"
        LECTURE = "LECTURE", "Lecture"

    class FileType(models.TextChoices):
        FILE = "FILE", "File"
        LINK = "LINK", "Link"

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    group = models.CharField(max_length=7, choices=FileGroup, default=FileGroup.LECTURE)
    type = models.CharField(max_length=4, choices=FileType, default=FileType.FILE)
    file = models.FileField(blank=True, null=True, upload_to=upload_file_path_handle, validators=[file_size])
    link = models.URLField(blank=True, null=True)
    inClass = models.ForeignKey(CourseClass, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

@receiver(models.signals.post_delete, sender=FileUpload)
def auto_delete_material(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(FileUpload, on_delete=models.CASCADE)
    text = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + ": " + self.text

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ForClass = models.ForeignKey(CourseClass, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.first_name + self.author.last_name + " - " + self.title