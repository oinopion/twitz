from django.views.generic import ListView
from statuses.forms import StatusForm
from statuses.models import Status

class TimelineView(ListView):
    queryset = Status.objects.all()
    context_object_name = 'statuses'
    template_name = 'statuses/timeline.html'

    def get_context_data(self, **kwargs):
        context = super(TimelineView, self).get_context_data(**kwargs)
        context['status_form'] = StatusForm()
        return context


timeline = TimelineView.as_view()

