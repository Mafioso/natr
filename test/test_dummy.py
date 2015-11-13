import json
import unittest2 as unittest
from faker import Factory
from rest_framework.test import APITestCase
from rest_framework import status

fake = Factory.create('ru_RU')


class ContactListTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		pass

	def test_dummy(self):
		self.assertEqual(True, True)

	@classmethod
	def tearDownClass(cls):
		pass


class DummyApiTestCase(APITestCase):

	def test_feed(self):
		response = self.client.get('/dummies/feed/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		content = json.loads(response.content)
		self.assertTrue(isinstance(content, list))
		self.assertTrue(content[0].has_key('dummy_1'))
		self.assertTrue(content[0].has_key('dummy_2'))
