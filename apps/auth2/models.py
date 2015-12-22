    #!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, **extra_fields)

    def create_natrexpert(self, email, password, **extra_fields):
        account = self._create_user(email, password, False, **extra_fields)
        return NatrUser.objects.create(account=account)


class Account(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(u'email', blank=True, unique=True)
    full_name = models.CharField(u'Ф.И.О.', max_length=30, blank=True)
    is_active = models.BooleanField(u'активирован', default=True)
    date_joined = models.DateTimeField(u'дата добавления', default=timezone.now)

    objects = UserManager()


    @property
    def is_staff(self):
        return self.is_superuser

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        "Returns the short name for the user."
        return self.full_name.split()[1]

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

class NatrUser(models.Model):

    DEFAULT_GROUPS = EXPERT, MANAGER, RISK_EXPERT = ('expert', 'manager', 'risk_expert')

    number_of_projects = models.IntegerField(u'Количество проектов', null=True)

    account = models.OneToOneField('Account', related_name='user')

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

    def is_admin(self):
        groups = self.get_groups()
        return groups.filter(name=NatrUser.ADMIN).first()

    def get_groups(self):
        return self.account.groups.all()


def assign_user_group(sender, instance, created=False, **kwargs):
    """If natr user does not belong to any group, assign expert by default."""
    if not created:
        return
    if instance.is_expert() or instance.is_manager() or instance.is_admin():
        return
    instance.add_to_experts()

post_save.connect(assign_user_group, sender=NatrUser)
