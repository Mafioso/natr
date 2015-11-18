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

