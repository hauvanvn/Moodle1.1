from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import User, OtpToken

# Register your models here.
class Userdata(ImportExportModelAdmin, admin.ModelAdmin):
    pass
    
class Otpdata(admin.ModelAdmin):
    pass
admin.site.register(User, Userdata)
admin.site.register(OtpToken, Otpdata)