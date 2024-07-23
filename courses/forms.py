from django import forms
from .models import FileUpload

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('id', 'name', 'group', 'type', 'file', 'link', 'inClass')