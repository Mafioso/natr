from django.db.models.signals import post_syncdb
import auth2.models
from django.contrib.auth.models import Group

def create_default_groups(sender, **kwargs):
	for def_group in auth2.models.NatrUser.DEFAULT_GROUPS:
		Group.objects.get_or_create(name=def_group)
		print 'GROUP created %s' % def_group


post_syncdb.connect(create_default_groups, sender=auth2.models)