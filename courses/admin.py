from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Course, CourseClass, FileUpload, Comment, Notification

# Register your models here.
class coursedata(ImportExportModelAdmin, admin.ModelAdmin):
    pass

admin.site.register(Course, coursedata)
admin.site.register(CourseClass, coursedata)
admin.site.register(FileUpload, coursedata)
admin.site.register(Comment, coursedata)
admin.site.register(Notification, coursedata)