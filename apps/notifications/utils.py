from django.conf import settings

def prepare_channel(uid):
	channel = getattr(settings, "NOTIFICATION_CHANNEL")
	return channel + "#" + uid