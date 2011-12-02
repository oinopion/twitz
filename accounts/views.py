from django.forms.forms import Form
from django.views.generic import FormView

class SettingsView(FormView):
    template_name = 'accounts/settings.html'
    form_class = Form

settings = SettingsView.as_view()
