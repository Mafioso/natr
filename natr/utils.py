import os
from datetime import datetime, time, timedelta
import factory
import random
import faker
from random import randrange
from django.utils import timezone as tz
from django.utils.dateparse import parse_date as dj_parse_date
from moneyed import Money, KZT

f = faker.Faker()


def fake_money():
    return Money(random.randint(1, 100) * 1000, KZT)

def zero_money():
    return Money(0, KZT)


def fake_url():
    host = f.url()[:-1]
    return os.path.join(host, fake_path())


def fake_path():
    uri = "/".join([f.uri() for _ in xrange(3)])
    return uri


def money_to_python(money_obj):
    return {
        'currency': money_obj.currency.code,
        'amount': money_obj.amount
    }


def pretty(d, indent=0):
    if isinstance(d, list) and d and hasattr(d[0], 'iteritems'):
        for item in d:
            pretty(item)
    else: 
        for key, value in d.iteritems():
            print u'\t' * indent + unicode(key)
            if hasattr(value, 'iteritems'):
                pretty(value, indent+1)
            else:
                if isinstance(value, list):
                    val = ""
                    for item in value:
                        if hasattr(item, 'iteritems'):
                            val += ", " + pretty(item, indent + 1)
                        else:
                            val += ", " + unicode(item)
                    value = val
                print u'\t' * (indent+1) + unicode(value)


        return ''

def get_stringed_value(value):
    if not value:
        return ""
    return '%s'%value


def make_aware(dt):
    return tz.is_aware(dt) and dt or tz.make_aware(dt)

def begin_of(dt):
    return make_aware(
        datetime.combine(dt.date(), time.min))


def end_of(dt):
    return make_aware(
        datetime.combine(dt.date(), time.max))


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return make_aware(start + timedelta(seconds=random_second))


def last_monthday(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month + 1, day=1) - timedelta(days=1)

def first_monthday(date):
    return date.replace(day=1)

def first_yearday(date):
    return date.replace(month=1, day=1)

def last_yearday(date):
    return date.replace(month=12, day=31)

def days_from_now(days):
    return days_from(tz.now(), days)

def days_from(dt, days):
    return make_aware(dt - timedelta(days=days))

def seconds_from(dt, sec):
    return make_aware(dt - timedelta(seconds=sec))    

def seconds_after(dt, sec):
    return make_aware(dt + timedelta(seconds=sec))

def days_range(from_dt, to_dt):
    for n in xrange(int((to_dt - from_dt).days + 1)):
        yield from_dt + timedelta(n)

def parse_date(dtstr):
    dt = dj_parse_date(dtstr)
    if not dt:
        return None
    return datetime.combine(dt, time.min)

