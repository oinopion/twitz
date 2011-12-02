from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

homepage = TemplateView.as_view(template_name='homepage.html')

urlpatterns = patterns('',
    url(r'^$', homepage, name='homepage'),
    url(r'^settings/', 'accounts.views.settings', name='settings'),
    url(r'^admin/', include(admin.site.urls)),
)
