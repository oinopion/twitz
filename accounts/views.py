from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView
from accounts.forms import SettingsForm

class SettingsView(UpdateView):
    template_name = 'accounts/settings.html'
    form_class = SettingsForm

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('settings')


settings = login_required(SettingsView.as_view())
