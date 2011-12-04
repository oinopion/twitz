# encoding: utf-8
from django import forms
from statuses.models import Status

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ('text', )

    def save(self, commit=True):
        if not self.instance.pk and getattr(self, 'author'):
            self.instance.author = self.author
        return super(StatusForm, self).save(commit)
