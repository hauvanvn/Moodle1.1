from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Course, CourseClass, FileUpload

# Register your models here.
class coursedata(ImportExportModelAdmin, admin.ModelAdmin):
    pass

admin.site.register(Course, coursedata)
admin.site.register(CourseClass, coursedata)