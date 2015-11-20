import json
import unittest2 as unittest
from faker import Factory
from rest_framework.test import APITestCase
from rest_framework import status


class DummyApiTestCase(APITestCase):

	def test_feed(self):
		self.assertTrue(True)
