from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'statuses.views.timeline', name='timeline'),
    url(r'^update/$', 'statuses.views.status_update', name='status_update'),
    url(r'^users/(?P<username>\w+)/$', 'statuses.views.user', name='user'),
    url(r'^settings/$', 'accounts.views.settings', name='settings'),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'logout_then_login', name='logout'),
)
