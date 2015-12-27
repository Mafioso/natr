    #!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xepa4ep'

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import get_app, get_models
from grantee.models import Grantee


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
        send_mail(
            u'Добро пожаловать в ИСЭМ',
            u"""Здравствуйте %(name)s!
            Ваши данные для входа в ИСЭМ:\n
            email: %(email)s,\n
            пароль: %(password)s\n\n.
            Ссылка для входа в кабинет: http://178.88.64.87:8000""" % {
                'name': account.get_full_name(),
                'email': email,
                'password': password
            },
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False
        )
        return acc

    def create_grantee(self, email, password, organization=None, **extra_fields):
        account = self._create_user(email, password, False, **extra_fields)
        grantee = Grantee.objects.create(
            account=account,
            organization=organization,)
        send_mail(
            u'Добро пожаловать в Кабинет Грантополучателя',
            u"""Здравствуйте %(name)s!
            Ваши данные для входа в Грантополучателя:\n
            email: %(email)s,\n
            пароль: %(password)s\n\n.
            Ссылка для входа в кабинет: http://178.88.64.87:8000""" % {
                'name': account.get_full_name(),
                'email': email,
                'password': password
            },
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False
        )
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


class NatrUser(models.Model):

    class Meta:
        relevant_for_permission = True
        verbose_name = u'Пользователи ИСЭМ'

    DEFAULT_GROUPS = EXPERT, MANAGER, RISK_EXPERT = ('expert', 'manager', 'risk_expert')

    DEPARTMENTS_CAPS = (
        u'Альтернативная энергетика и технологии энергоэффективности',
        u'Биотехнологии',
        u'Инфокоммуникационные технологии',
        u'Прогрессивные технологии в агропромышленном комплексе',
        u'Прогрессивные технологии машиностроения, включая использование новых материалов',
        u'Прогрессивные технологии химии и нефтехимии',
        u'Прогрессивные технологии поиска, добычи, транспортировки и переработки минерального и углеводородного сырья',
        u'Прогрессивные технологии в горно-металлургическом комплексе',
        u'Стройиндустрия')
    DEPARTMENTS_OPTS = zip(range(len(DEPARTMENTS_CAPS)), DEPARTMENTS_CAPS)

    department = models.IntegerField(null=True, choices=DEPARTMENTS_OPTS)

    account = models.OneToOneField('Account', related_name='user')

    def get_department_cap(self):
        try:
            return NatrUser.DEPARTMENTS_CAPS[self.department]
        except TypeError:
            return None

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


def assign_user_group(sender, instance, created=False, **kwargs):
    """If natr user does not belong to any group, assign expert by default."""
    if not created:
        return
    if instance.is_expert() or instance.is_manager() or instance.is_risk_expert():
        return
    instance.add_to_experts()

def on_natruser_delete(sender, instance, *a, **kw):
    try:
        instance.account.delete()
    except ObjectDoesNotExist:
        return None

post_save.connect(assign_user_group, sender=NatrUser)

post_delete.connect(on_natruser_delete, sender=NatrUser)
