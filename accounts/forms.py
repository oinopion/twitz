# encoding: utf-8
from django import forms
from accounts.models import Profile

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

