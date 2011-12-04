# encoding: utf-8
from django.contrib import admin
from accounts.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'time_zone')
    list_display_links = ('pk', 'user')
    readonly_fields = ('user',)


admin.site.register(Profile, ProfileAdmin)
