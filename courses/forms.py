from django import forms
from .models import FileUpload, Notification

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('id', 'name', 'group', 'type', 'file', 'link', 'inClass')

class AnnouncementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].required = False

    class Meta:
        model = Notification
        # fields = '__all__'
        fields = ('title', 'text')