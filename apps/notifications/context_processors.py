from django.conf import settings
from notifications import utils


def main(request):
	print request.user, 'hi'
	return dict(
		NOTIFICATION_CHANNEL=utils.prepare_channel(request.user.pk)
	)