from django.test import TestCase
from datetime import timedelta
from django.utils import timezone as tz
from natr import utils
from chat.models import TextLine
from chat import models
from chat.factories import TextLine as TextLineFactory
from auth2.factories import Account as AccountFactory
from django.conf import settings


class TextLineTestCase(TestCase):
    
    @property
    def random_text_line(self):
        return TextLineFactory.build()

    def test_set_ts(self):
        line = self.random_text_line
        ts = utils.days_from(tz.now(), 15)
        line.set_ts(ts, force_save=False)
        self.assertEqual(ts, line.ts)

    def test_prepare_data(self):
        line = self.random_text_line
        
        def test_equals(obj, params):
            self.assertEqual(obj.line, params['line'])
            self.assertEqual(obj.ts, params['ts'])
            self.assertEqual(obj.from_account_id, params['from_account'])
            self.assertEqual(obj.to_account_id, params['to_account'])
        
        test_equals(line, line.prepare_data())
        
        # with attachments
        line = TextLineFactory.create()
        params = line.prepare_data(line.attachments.all())
        test_equals(line, params)
        actual = set([a['id'] for a in params['attachments']])
        expected = set([a.id for a in line.attachments.all()])
        self.assertEqual(actual, expected)

    def test_prepare_channel(self):
        mask = settings.CHAT_CHANNEL + "#{}"
        self.assertEqual(models.prepare_channel(1), mask.format(1))

    def test_concat_msg(self):
        cases = [
            (('', 'h'), 'h'),
            (('h', 'h'), 'h\nh'),
            (('h', ''), 'h'),
            (('', ''), ''),
        ]

        for act, exp in cases:
            self.assertEqual(models.concat_msg(act[0], act[1]), exp)

    def test_in_time_bounds(self):
        threshold = 200
        now = tz.now()
        cases = [
            ((utils.seconds_from(now, 15), now), True),
            ((utils.seconds_from(now, threshold), now), True),
            ((utils.seconds_from(now, threshold + 1), now), False),
            ((utils.seconds_from(now, 0), now), True),
        ]
        for act, exp in cases:
            self.assertEqual(models.in_time_bounds(act[0], act[1], threshold=threshold), exp)

    def test_of_user(self):
        u = AccountFactory.create(email='r.kamun@gmail.com')
        other_u = AccountFactory.create(email='vasya@pupkin.kz')
        n = 5

        def get_kwargs(i):
            return {
                'from_account': i % 2 == 1 and u or other_u,
                'to_account': i % 2 == 0 and u or other_u,
            }

        lines = [TextLineFactory.create(**get_kwargs(i)) for i in xrange(n)]
        qs = TextLine.objects.of_user(u)
        self.assertEqual(qs.count(), len(lines))

        qs = TextLine.objects.of_sender(u)
        self.assertEqual(qs.count(), n / 2)

        line = TextLine.objects.last_of_sender(u)
        self.assertIsNotNone(line)
        exp_line = TextLine.objects.of_sender(u).order_by('-ts').first()
        self.assertEqual(line, exp_line)

    def test_update_or_create(self):
        u = AccountFactory.create(email='r.kamun@gmail.com')
        other_u = AccountFactory.create(email='vasya@pupkin.kz')
        test_line = 'lorem'
        # 1. force_create
        created, line = TextLine.objects.update_or_create(
            u, line='test_line', force_create=True)
        self.assertTrue(created)
        self.assertTrue(line.id > 0)
        line.delete()
        # 2. no prev msg
        ts = tz.now()
        created, _ = TextLine.objects.update_or_create(
            u, line='test_line', ts=ts, force_create=False)
        self.assertTrue(created)
        # 3. not in time bounds
        created, line = TextLine.objects.update_or_create(
            u, line='one_more_line', ts=utils.seconds_after(ts, 2), threshold=1, force_create=False)
        self.assertTrue(created)
        line.delete()
        # 4. not same sender
        created, line = TextLine.objects.update_or_create(
            u, line='one_more_line', ts=utils.seconds_after(ts, 2), threshold=3, force_create=False, to_account=other_u)
        self.assertTrue(created)
        line.delete()
        # 5. update
        created, line = TextLine.objects.update_or_create(
            u, line='one_more_line', ts=utils.seconds_after(ts, 2), threshold=3, force_create=False)
        self.assertFalse(created)
        self.assertEqual(len(line.line.split('\n')), 2)
        # 6. attachments
        
