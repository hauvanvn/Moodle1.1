from django import forms
from .models import FileUpload, Notification, Assignment
from django_ckeditor_5.widgets import CKEditor5Widget

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('id', 'name', 'group', 'type', 'file', 'link', 'inClass')

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Notification
        # fields = '__all__'
        fields = ('title', 'text', 'author', 'ForClass')
        widgets = {
            'text': CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('author', 'ForClass', 'title', 'file', 'date_closed')