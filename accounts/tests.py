# encoding: utf-8
from django import forms
from django.test import TestCase
from accounts.forms import SettingsForm
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


class SettingsViewTest(TestCase):
    def test_get_is_successful(self):
        self.assertEqual(self.get().status_code, 200)

    def test_get_is_successful(self):
        self.assertTemplateUsed(self.get(), 'accounts/settings.html')

    def get(self):
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
