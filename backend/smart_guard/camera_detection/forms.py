from django import forms
from .models import Capture

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Capture
        fields = ['photo']

class UploadVideoForm(forms.ModelForm):
    class Meta:
        model = Capture
        fields = ['video']

class UploadBothForm(forms.ModelForm):
    class Meta:
        model = Capture
        fields = ['photo', 'video']
