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
    slug = models.SlugField()

    def __str__(self):
        return Course.get_deferred_fields(self=self.course) + '_' + self.className

class FileUpload():
    file = models.FileField()
    inClass = models.ForeignKey(CourseClass, on_delete=models.CASCADE, blank=True, null=True)