    #!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import get_app, get_models
from grantee.models import Grantee
from natr import mailing


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
        return self._create_user(email, password, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, **extra_fields)

    def create_natrexpert(self, email, password, **extra_fields):
        account = self._create_user(email, password, False, **extra_fields)
        acc = NatrUser.objects.create(account=account)
        mailing.send_create_natrexpert(account.get_full_name(), email, password)
        return acc

    def create_grantee(self, email, password, organization=None, **extra_fields):
        account = self._create_user(email, password, False, **extra_fields)
        grantee = Grantee.objects.create(
            account=account,
            organization=organization,)
        mailing.send_create_grantee(account.get_full_name(), email, password)
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
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

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


class Department(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)


class NatrUser(models.Model):

    class Meta:
        relevant_for_permission = True
        verbose_name = u'Пользователи ИСЭМ'

    DEFAULT_GROUPS = EXPERT, MANAGER, RISK_EXPERT = ('expert', 'manager', 'risk_expert')

    departments = models.ManyToManyField(Department, blank=True)

    account = models.OneToOneField('Account', related_name='user', on_delete=models.CASCADE)

    def delete(self, **kwargs):
        acc = self.account
        super(NatrUser, self).delete(**kwargs)
        acc.delete()

    def get_full_name(self):
        return self.account.get_full_name()

    def add_to_experts(self):
        group = Group.objects.get(name=NatrUser.EXPERT)
        self.account.groups.add(group)
        return self

    def is_expert(self):
        groups = self.get_groups()
        return groups.filter(name=NatrUser.EXPERT).first()

    def is_manager(self):
        groups = self.get_groups()
        return groups.filter(name=NatrUser.MANAGER).first()

    def is_risk_expert(self):
        groups = self.get_groups()
        return groups.filter(name=NatrUser.RISK_EXPERT).first()

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
    if instance.is_expert() or instance.is_manager() or instance.is_risk_expert():
        return
    instance.add_to_experts()

post_save.connect(assign_user_group, sender=NatrUser)


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
