from django.conf import settings

def prepare_channel(uid, channel=None):
	channel = channel if channel is not None else getattr(settings, "NOTIFICATION_CHANNEL")
	return "{}#{}".format(channel, uid)