from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView
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


timeline = TimelineView.as_view()
status_update = login_required(StatusUpdateView.as_view())
