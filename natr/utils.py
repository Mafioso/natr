import os
import factory
import random
import faker
from moneyed import Money, KZT

f = faker.Faker()


def fake_money():
    return Money(random.randint(1, 100) * 1000, KZT)


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


