from django.db import models
from users.models import User

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

    def __str__(self):
        return Course.get_deferred_fields(self=self.course) + '_' + self.className

class FileUpload(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField()
    inClass = models.ForeignKey(CourseClass, on_delete=models.CASCADE, blank=True, null=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(FileUpload, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return User.get_deferred_fields(self=self.user) + self.text

class Notification(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ForClass = models.ManyToManyField(CourseClass)
    text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return User.get_deferred_fields(self=self.author) + self.text