import unittest2 as unittest
from faker import Factory

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
