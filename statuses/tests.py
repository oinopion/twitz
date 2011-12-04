# encoding: utf-8
from django.contrib.auth.models import User
from mock import patch
from django.core.exceptions import ValidationError
from django.test import TestCase
from statuses.forms import StatusForm
from statuses.models import Status


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


class TimelineView(TestCase):
    def test_renders_template(self):
        self.assertTemplateUsed(self.get(), 'statuses/timeline.html')

    def test_gives_statuses_to_template(self):
        self.assertIn("statuses", self.get().context)

    def test_gives_form_to_template(self):
        self.assertIn("status_form", self.get().context)

    def test_renders_recent_statuses(self):
        msg = "Hello, World-%d!"
        statuses = [create_status(text=msg % n) for n in xrange(5)]
        resp = self.get()
        for status in statuses:
            self.assertContains(resp, status.text)

    def get(self):
        return self.client.get('/')


class StatusFormTest(TestCase):
    def test_is_valid_with_text(self):
        f = StatusForm({'text': 'What is your quest?'})
        self.assertTrue(f.is_valid())

    def test_sets_correct_author(self):
        u = User.objects.create_user("jack")
        f = StatusForm({'text': 'What is your quest?'})
        self.assertEqual(u, f.save(author=u).author)

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
