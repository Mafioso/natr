import os
from datetime import datetime, time, timedelta
import factory
import random
import faker
from random import randrange
from django.utils import timezone as tz
from django.utils.dateparse import parse_date as dj_parse_date
from moneyed import Money, KZT
from collections import OrderedDict

f = faker.Faker()

def get_date_query_range(datetime_value):
    return (tz.make_aware(datetime.combine(datetime_value, time.min)), 
            tz.make_aware(datetime.combine(datetime_value, time.max)))

def get_field_display(klass, field, value):
    f = klass._meta.get_field(field)
    return dict(f.flatchoices).get(value, value)

def print_itertools(items):
    def prnt(item):
        print item
    map(prnt, items)

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
    if not value and value != 0:
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

def very_old_dt():
    return tz.now().replace(year=1970)

def parse_date(dtstr):
    dt = dj_parse_date(dtstr)
    if not dt:
        return None
    return datetime.combine(dt, time.min)

def write_roman(num):

    roman = OrderedDict()
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num > 0:
                roman_num(num)
            else:
                break

    return "".join([a for a in roman_num(num)])

def getRatio(numerator, denominator):
    if denominator == 0 or \
        numerator == None or \
        denominator == None:
        return ""

    print numerator, denominator
    return "%.2f%%"%(numerator/denominator*100)
