import factory
import random
from moneyed import Money, KZT


def fake_money():
	return Money(random.randint(1, 100) * 1000, KZT)
