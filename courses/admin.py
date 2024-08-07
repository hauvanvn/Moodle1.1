from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Course, CourseClass, FileUpload, Comment, Notification, Assignment, Submission

# Register your models here.
class coursedata(ImportExportModelAdmin, admin.ModelAdmin):
    pass

admin.site.register(Course, coursedata)
admin.site.register(CourseClass, coursedata)
admin.site.register(FileUpload, coursedata)
admin.site.register(Comment, coursedata)
admin.site.register(Notification, coursedata)
admin.site.register(Assignment, coursedata)
admin.site.register(Submission, coursedata)