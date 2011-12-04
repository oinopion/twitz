# encoding: utf-8
from django.contrib import admin
from statuses.models import Status

class StatusAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'pub_date')
    list_display_links = ('pk', 'text')
    date_hierarchy = 'pub_date'
    ordering = ('-pub_date',)

admin.site.register(Status, StatusAdmin)
