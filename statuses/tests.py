# encoding: utf-8
from django.contrib.auth.models import User
from mock import patch
from django.core.exceptions import ValidationError
from django.test import TestCase
from statuses.forms import StatusForm
from statuses.models import Status

class LoginViewMixin(object):
    def login(self):
        self.user = User.objects.create_user("jill", password="jill")
        self.client.login(username="jill", password="jill")


class StatusModelTest(TestCase):
    def test_requires_author_and_text(self):
        try:
            Status().full_clean()
        except ValidationError as e:
            self.assertIn("author", e.message_dict)
            self.assertIn("text", e.message_dict)
        else:
            self.fail("Status misses some required fields")

    @patch('django.utils.timezone.datetime')
    def test_pub_date_has_default(self, now):
        s = Status()
        self.assertEqual(now.utcnow().replace(), s.pub_date)

    def test_timeline_query_is_ordered(self):
        q = Status.objects.timeline()
        self.assertSequenceEqual(['-pub_date'], q.query.order_by)

    def test_timeline_query_is_limited(self):
        q = Status.objects.timeline()
        self.assertEqual(0, q.query.low_mark)
        self.assertEqual(20, q.query.high_mark)


class TimelineView(TestCase, LoginViewMixin):
    def test_renders_template(self):
        self.assertTemplateUsed(self.get(), 'statuses/timeline.html')

    def test_gives_statuses_to_template(self):
        self.assertIn("statuses", self.get().context)

    def test_uses_good_queryset(self):
        sql = str(self.get().context['statuses'].query)
        self.assertEqual(str(Status.objects.timeline().query), sql)

    def test_gives_form_to_template(self):
        self.assertIn("status_form", self.get().context)

    def test_renders_recent_statuses(self):
        msg = "Hello, World-%d!"
        statuses = [create_status(text=msg % n) for n in xrange(5)]
        resp = self.get()
        for status in statuses:
            self.assertContains(resp, status.text)

    def test_renders_form_when_logged_in(self):
        self.login()
        self.assertContains(self.get(), '<form class="status-form')

    def test_does_not_render_form_when_not_logged_in(self):
        self.assertNotContains(self.get(), '<form class="status-form')

    def get(self):
        return self.client.get('/')


class UserViewTest(TestCase):
    def test_get(self):
        self.assertTemplateUsed(self.get(), 'statuses/user.html')

    def test_template_gets_user(self):
        self.assertIn('observed_user', self.get().context)

    def test_template_gets_statuses(self):
        self.assertIn('statuses', self.get().context)

    def get(self):
        u = User.objects.create_user('mike')
        return self.client.get(u.get_absolute_url())


class StatusUpdateView(TestCase, LoginViewMixin):
    def test_requires_login(self):
        resp = self.client.get('/update/')
        self.assertRedirects(resp, '/login/?next=/update/')

    def test_redirects(self):
        self.assertRedirects(self.post(text="Hello"), '/')

    def test_creates_status(self):
        self.post(text="Hello")
        self.assertTrue(self.user.status_set.exists())

    def test_renders_template(self):
        self.assertTemplateUsed(self.get(), 'statuses/status_form.html')

    def post(self, **kwargs):
        self.login()
        return self.client.post('/update/', kwargs)

    def get(self):
        self.login()
        return self.client.get('/update/')



class StatusFormTest(TestCase):
    def test_is_valid_with_text(self):
        f = StatusForm({'text': 'What is your quest?'})
        self.assertTrue(f.is_valid())

    def test_is_not_valid_with_too_long_text(self):
        f = StatusForm({'text': 'a' * 257})
        self.assertFalse(f.is_valid())


    def test_sets_correct_author(self):
        f = StatusForm({'text': 'What is your quest?'})
        f.author = User.objects.create_user("jack")
        self.assertEqual(f.author, f.save().author)

    def test_unbound_instance(self):
        self.assertFalse(StatusForm().is_bound)


def create_status(**kwargs):
    try:
        author = kwargs.get('author') or User.objects.get(username="john")
    except User.DoesNotExist:
        author = User.objects.create_user("john")
    defaults = {'author': author, 'text': "Hello, world!"}
    defaults.update(kwargs)
    return Status.objects.create(**defaults)
