from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import User

# Register your models here.
class Userdata(ImportExportModelAdmin, admin.ModelAdmin):
    pass
    
admin.site.register(User, Userdata)