# encoding: utf-8
from django import forms
from statuses.models import Status

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ('text', )

    def save(self, author, commit=True):
        if not self.instance.pk:
            self.instance.author = author
        return super(StatusForm, self).save(commit)
