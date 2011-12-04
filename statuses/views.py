from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.decorators import login_required

from statuses.forms import StatusForm
from statuses.models import Status

class TimelineView(ListView):
    queryset = Status.objects.timeline()
    context_object_name = 'statuses'
    template_name = 'statuses/timeline.html'

    def get_context_data(self, **kwargs):
        context = super(TimelineView, self).get_context_data(**kwargs)
        context['status_form'] = StatusForm()
        return context


class StatusUpdateView(CreateView):
    model = Status
    form_class = StatusForm

    def form_valid(self, form):
        form.author = self.request.user
        return super(StatusUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('timeline')


class UserView(DetailView):
    model = User
    context_object_name = 'observed_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'statuses/user.html'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        user = self.object
        context['statuses'] = user.status_set.timeline()[:20]
        context['same_user'] = user == self.request.user
        return context


timeline = TimelineView.as_view()
status_update = login_required(StatusUpdateView.as_view())
user = UserView.as_view()
