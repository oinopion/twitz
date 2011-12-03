# encoding: utf-8
from django.utils import timezone
from accounts.models import Profile

class TimeZoneMiddleware:
    def process_request(self, request):
        if request.user and request.user.is_authenticated():
            try:
                timezone.activate(request.user.profile.time_zone)
            except Profile.DoesNotExist:
                pass
            except ValueError:
                pass
