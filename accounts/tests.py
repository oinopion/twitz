# encoding: utf-8
from django import forms
import django
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.timezone import get_default_timezone, get_current_timezone, deactivate, get_current_timezone_name
from accounts.forms import SettingsForm
from accounts.middlewares import TimeZoneMiddleware
from accounts.models import Profile, User

class ProfileModelTest(TestCase):
    def test_new_user_has_profile(self):
        p = User.objects.create_user("john").profile
        self.assertIsInstance(p, Profile)

    def test_second_user_gets_new_profile(self):
        a = User.objects.create_user("alice").profile
        b = User.objects.create_user("bob").profile
        self.assertNotEqual(a, b)

    def test_profile_is_deleted_with_user(self):
        profile = User.objects.create_user("luke").profile
        profile.user.delete()
        self.assertFalse(Profile.objects.filter(pk=profile.pk).exists())

    def test_profile_time_zone_validation(self):
        profile = Profile()
        profile.time_zone = "adsfasdf"
        try:
            profile.full_clean()
        except ValidationError, e:
            self.assertIn('time_zone', e.message_dict)
        else:
            self.fail("Should raise validation error")


class SettingsViewTest(TestCase):
    def test_requires_logged_in_user(self):
        client = self.client_class()
        self.assertRedirects(client.get('/settings/'),
                             '/login/?next=/settings/')

    def test_get_is_successful(self):
        self.assertEqual(self.get().status_code, 200)

    def test_get_is_successful(self):
        self.assertTemplateUsed(self.get(), 'accounts/settings.html')

    def test_has_form(self):
        context = self.get().context
        self.assertIn('form', context)
        self.assertIsInstance(context['form'], SettingsForm)

    def test_renders_form(self):
        resp = self.get()
        self.assertContains(resp, 'form class="settings"')
        self.assertContains(resp, 'select name="time_zone"')

    def test_post_is_successful(self):
        resp = self.post({'time_zone': "UTC"})
        self.assertRedirects(resp, '/settings/')

    def test_saves_profile(self):
        casablanca = 'Africa/Casablanca'
        self.post({'time_zone': casablanca})
        self.assertEqual(self.user.profile.time_zone, casablanca)

    def post(self, data):
        self.user = User.objects.create_user("john", password="john")
        self.client.login(username="john", password="john")
        return self.client.post('/settings/', data)

    def get(self):
        self.user = User.objects.create_user("john", password="john")
        self.client.login(username="john", password="john")
        return self.client.get('/settings/')


class SettingsFormTest(TestCase):
    def test_creation(self):
        form = SettingsForm()
        self.assertIsInstance(form, forms.ModelForm)

    def test_has_time_zone(self):
        form = SettingsForm()
        self.assertTrue(form.fields['time_zone'])

    def test_save_valid(self):
        for time_zone in ('UTC', 'Europe/Warsaw', 'America/Chicago'):
            form = SettingsForm({'time_zone': time_zone})
            self.assertTrue(form.is_valid())

    def test_not_valid(self):
        form = SettingsForm({'time_zone': 'NO SUCH TIME ZONE'})
        self.assertFalse(form.is_valid())


class TimeZoneMiddlewareTest(TestCase):
    def setUp(self):
        self.middleware = TimeZoneMiddleware()
        deactivate() # clean up after other tests

    def tearDown(self):
        deactivate() 

    def test_does_noet_set_tz_if_no_user(self):
        req = self.anonymous_request()
        self.middleware.process_request(req)
        self.assertEqual(get_default_timezone(), get_current_timezone())

    def test_sets_users_time_zone(self):
        req = self.request_with_time_zone('Africa/Juba')
        self.middleware.process_request(req)
        self.assertEqual(get_current_timezone_name(), 'Africa/Juba')

    def test_works_with_non_time_zone(self):
        req = self.request_with_time_zone(None)
        self.middleware.process_request(req)
        self.assertEqual(get_default_timezone(), get_current_timezone())

    def test_works_with_bad_time_zone(self):
        req = self.request_with_time_zone('NON_TIME_ZONE_STRING')
        self.middleware.process_request(req)
        self.assertEqual(get_default_timezone(), get_current_timezone())

    def test_is_configured(self):
        middlewares = django.conf.settings.MIDDLEWARE_CLASSES
        self.assertIn('accounts.middlewares.TimeZoneMiddleware', middlewares)

    def request_with_time_zone(self, time_zone):
        req = RequestFactory().request()
        req.user = User.objects.create_user("josh")
        req.user.profile.time_zone = time_zone
        return req

    def anonymous_request(self):
        req = RequestFactory().request()
        req.user = AnonymousUser()
        return req
