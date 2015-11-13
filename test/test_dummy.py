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
