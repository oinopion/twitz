from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

homepage = TemplateView.as_view(template_name='homepage.html')

urlpatterns = patterns('',
    url(r'^$', homepage, name='homepage'),
    url(r'^settings/$', 'accounts.views.settings', name='settings'),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'logout_then_login', name='logout'),
)
