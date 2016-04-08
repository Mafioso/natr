# -*- coding: utf-8 -*-
from django.db.models.signals import post_syncdb
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from natr.models import NatrGroup
import auth2.models

def create_default_groups(sender, **kwargs):
	for def_group in NatrGroup.ROLES:
		group = NatrGroup.objects.get_or_create(name=def_group)[0]
		if def_group == NatrGroup.ADMIN:
			group.permissions = Permission.objects.all()
			group.save()
			print '%s permissions added into admin group' % group.permissions.count()
		print 'GROUP (NatrGroup) created %s' % def_group


post_syncdb.connect(create_default_groups, sender=auth2.models)


def add_view_permissions(sender, **kwargs):
	"""
	This syncdb hooks takes care of adding a view permission too all our
	content types.
	"""
	# for each of our content types
	for content_type in ContentType.objects.all():
		# build our permission slug
		codename = "view_%s" % content_type.model

		# if it doesn't exist..
		if not Permission.objects.filter(content_type=content_type, codename=codename):
			# add it
			Permission.objects.create(content_type=content_type,
									  codename=codename,
									  name="Can view %s" % content_type.name)
			# print "Added view permission for %s" % content_type.name

# check for all our view permissions after a syncdb
post_syncdb.connect(add_view_permissions)
