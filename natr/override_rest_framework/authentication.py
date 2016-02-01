from rest_framework.authentication import BaseAuthentication, TokenAuthentication as RestTokenAuthentication
from integrations.models import Token
from rest_framework import exceptions


class DummyUser(object):
	
	def is_authenticated(self):
		return True


class DummyAuthentication(BaseAuthentication):

	def authenticate(self, request):
		return (DummyUser(), None)


class TokenAuthentication(RestTokenAuthentication):

    model = Token


    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.select_related('account').get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        if not token.account.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (token.account, token)