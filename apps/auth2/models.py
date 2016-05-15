    #!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.db.models import get_app, get_models
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from grantee.models import Grantee
from natr import mailing
from natr.models import NatrGroup
from notifications.models import NotificationCounter


def get_relevant_permissions():
    models = []
    for app_name in settings.APPS:
        models.extend(
            filter(lambda x: getattr(x._meta, 'relevant_for_permission', False), get_models(
                get_app(app_name)))
        )
    cttypes = ContentType.objects.get_for_models(*models).values()
    return Permission.objects.filter(content_type__in=cttypes)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        groups = extra_fields.pop('groups', [])
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user.groups.add(*groups)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        admin_group = NatrGroup.objects.filter(name=NatrGroup.ADMIN).first()
        admin_group.permissions = Permission.objects.all()
        admin_group.save()

        groups = extra_fields.pop('groups', [admin_group])
        extra_fields['groups'] = groups
        acc = self._create_user(email, password, True, **extra_fields)
        user = NatrUser.objects.create(account=acc)
        return user

    def create_natrexpert(self, email, password, **extra_fields):
        account = self._create_user(email, password, False, **extra_fields)
        user = NatrUser.objects.create(account=account)
        try:
            mailing.send_create_natrexpert(account.get_full_name(), email, password)
        except Exception as e:
            print str(e)
        return user

    def create_grantee(self, email, password, organization=None, **extra_fields):
        groups = extra_fields.pop('groups', [NatrGroup.objects.get(name=NatrGroup.GRANTEE)])
        extra_fields['groups'] = groups

        account = self._create_user(email, password, False, **extra_fields)
        grantee = Grantee.objects.create(
            account=account,
            organization=organization,)
        try:
            mailing.send_create_grantee(account.get_full_name(), email, password)
        except Exception as e:
            print str(e)
        return grantee

class Account(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(u'email', blank=True, unique=True)
    first_name = models.CharField(u'Имя', max_length=30, blank=True, null=True)
    last_name = models.CharField(u'Фамилия', max_length=30, blank=True, null=True)
    is_active = models.BooleanField(u'активирован', default=True)
    date_joined = models.DateTimeField(u'дата добавления', default=timezone.now)

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_superuser

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = ' '.join( filter(None, [self.first_name, self.last_name]) )
        return unicode(full_name.strip())

    def get_short_name(self):
        "Returns the short name for the user."
        return unicode(self.first_name)

    def get_counters(self):
        return {
            'notif': {
                'id': self.notif_counter.id,
                'counter': self.notif_counter.counter
            }
        }

    def get_all_permission_objs(self):
        perms = {p.id: p for p in self.user_permissions.all()}
        for p in Permission.objects.filter(group__in=self.groups.all()):
            perms.setdefault(p.id, p)
        return perms.values()

    @property
    def get_user_type(self):
        if hasattr(self, 'user'):
            if self.user.is_director():
                return NatrGroup.DIRECTOR
            elif self.user.is_manager():
                return NatrGroup.MANAGER
            elif self.user.is_expert():
                return NatrGroup.EXPERT
            elif self.user.is_risk_expert():
                return NatrGroup.RISK_EXPERT
            elif self.user.is_independent_expert():
                return NatrGroup.INDEPENDENT_EXPERT
            else:
                return NatrGroup.EXPERT
        elif hasattr(self, 'grantee'):
            return 'grantee'


class Department(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)


class NatrUser(models.Model):

    class Meta:
        relevant_for_permission = True
        verbose_name = u'Пользователи ИСЭМ'

    departments = models.ManyToManyField(Department, blank=True)

    account = models.OneToOneField('Account', related_name='user', on_delete=models.CASCADE)

    def get_full_name(self):
        return self.account.get_full_name()

    def add_to_experts(self):
        group = NatrGroup.objects.get(name=NatrGroup.EXPERT)
        self.account.groups.add(group)
        return self

    def is_expert(self):
        groups = self.get_groups()
        return groups.filter(name=NatrGroup.EXPERT).first()

    def is_director(self):
        groups = self.get_groups()
        return groups.filter(name=NatrGroup.DIRECTOR).first()

    def is_manager(self):
        groups = self.get_groups()
        return groups.filter(name=NatrGroup.MANAGER).first() or groups.filter(name=NatrGroup.DIRECTOR).first()

    def is_admin(self):
        groups = self.get_groups()
        return groups.filter(name=NatrGroup.ADMIN).first()

    def is_risk_expert(self):
        groups = self.get_groups()
        return groups.filter(name=NatrGroup.RISK_EXPERT).first()

    def is_independent_expert(self):
        groups = self.get_groups()
        return groups.filter(name=NatrGroup.INDEPENDENT_EXPERT).first()

    def get_groups(self):
        return self.account.groups.all()

    def add_to_groups(self, groups):
        self.account.groups.add(*groups)
        return self

    @classmethod
    def test_cascade(cls):
        test_cascade()


def assign_user_group(sender, instance, created=False, **kwargs):
    """If natr user does not belong to any group, assign expert by default."""
    if not created:
        return
    if instance.is_expert() or instance.is_manager() or instance.is_risk_expert() or instance.is_director() or instance.is_independent_expert():
        return
    instance.add_to_experts()

def delete_account(sender, instance, **kwargs):
    instance.account.delete()

def set_new_perm_to_admin(sender, instance, created=False, **kwargs):
    if not created:
        return
    admin_group, created = NatrGroup.objects.get_or_create(name=NatrGroup.ADMIN)
    if admin_group:
        admin_group.permissions.add(instance)
    print 'added new perm to NatrGroup.ADMIN', instance


@receiver(post_save, sender=Account)
def on_user_create(sender, instance, created=False, **kwargs):
	if not created:
		return   # not interested
	NotificationCounter.get_or_create(instance)


post_save.connect(assign_user_group, sender=NatrUser)
post_delete.connect(delete_account, sender=NatrUser)
post_save.connect(set_new_perm_to_admin, sender=Permission)

def test_cascade():
    import random
    email = 'aa{}@ya.ru'.format(random.randint(1, 10000000))
    a = Account(email=email)
    a.set_password('123')
    a.save()

    u = NatrUser.objects.create(account=a)
    u.save()
    uid = u.pk

    a.delete()
    try:
        NatrUser.objects.get(pk=uid).delete()
        assert False, 'Cascade is not working'
    except NatrUser.DoesNotExist:
        print 'Cascade WORKS!!!'
