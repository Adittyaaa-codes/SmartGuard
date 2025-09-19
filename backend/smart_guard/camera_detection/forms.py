from django import forms
from .models import Capture

class ImageForm(forms.ModelForm):
    weapon_name = forms.CharField(required=False, initial='None', max_length=100, label="Weapon Name")
    weapon_number = forms.IntegerField(required=False, initial=0, min_value=0, label="Weapon Number")

    class Meta:
        model = Capture
        fields = ['photo', 'weapon_name', 'weapon_number']

class VideoForm(forms.ModelForm):
    weapon_name = forms.CharField(required=False, initial='None', max_length=100, label="Weapon Name")
    weapon_number = forms.IntegerField(required=False, initial=0, min_value=0, label="Weapon Number")

    class Meta:
        model = Capture
        fields = ['video', 'weapon_name', 'weapon_number']

class BothForm(forms.ModelForm):
    weapon_name = forms.CharField(required=False, initial='None', max_length=100, label="Weapon Name")
    weapon_number = forms.IntegerField(required=False, initial=0, min_value=0, label="Weapon Number")

    class Meta:
        model = Capture
        fields = ['photo', 'video', 'weapon_name', 'weapon_number']
