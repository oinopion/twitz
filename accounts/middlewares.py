# encoding: utf-8
import logging
from django.utils import timezone
from pytz.exceptions import UnknownTimeZoneError
from accounts.models import Profile

logger = logging.getLogger(__name__)

class TimeZoneMiddleware:
    def process_request(self, request):
        if request.user and request.user.is_authenticated():
            try:
                timezone.activate(request.user.profile.time_zone)
            except (UnknownTimeZoneError, ValueError) as e:
                logger.warn("Error setting time zone: %s", e)
            except Profile.DoesNotExist:
                logger.error("No profile for user: %s", request.user.pk)
