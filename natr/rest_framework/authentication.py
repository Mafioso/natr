from rest_framework.authentication import BaseAuthentication

class DummyUser(object):
	
	def is_authenticated(self):
		return True


class DummyAuthentication(BaseAuthentication):

	def authenticate(self, request):
		return (DummyUser(), None)
