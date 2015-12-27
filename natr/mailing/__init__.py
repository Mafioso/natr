# -*- coding: utf-8 -*-
import os

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

def send_create_natrexpert(name, email, password):
    send_mail(
        u'Добро пожаловать в ИСЭМ',
        u"""Здравствуйте %(name)s!
        Ваши данные для входа в ИСЭМ:\n
        email: %(email)s,\n
        пароль: %(password)s\n\n.
        Ссылка для входа в кабинет: http://178.88.64.87:8000""" % {
            'name': name,
            'email': email,
            'password': password
        },
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )

def send_create_grantee(name, email, password):
    send_mail(
        u'Добро пожаловать в Кабинет Грантополучателя',
        u"""Здравствуйте %(name)s!
        Ваши данные для входа в Грантополучателя:\n
        email: %(email)s,\n
        пароль: %(password)s\n\n.
        Ссылка для входа в кабинет: http://178.88.64.87:8000""" % {
            'name': name,
            'email': email,
            'password': password
        },
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )

def send_milestone_status_payment(milestone):
    mail = EmailMessage(
                u'Смена статуса этапа по проекту \"%s\"' % milestone.project.name,
                u"""Здравствуйте!\nНачался этап №1 по вашему проекту \"%s\". Просим ознакомится с памяткой""" % milestone.project.name, 
                settings.DEFAULT_FROM_EMAIL,
                map(lambda x: x.account.email, milestone.project.organization_details.grantee_set.all())
            )
    attachment = open(
        os.path.join(os.path.abspath(settings.BASE_DIR), 'static', 'files', 'pamyatka.doc'), 'rb')
    mail.attach(os.path.basename(attachment.name), attachment.read(), 'application/msword')
    mail.send(fail_silently=False)

def send_milestone_status_implementation(milestone):
    send_mail(
        u'Смена статуса этапа по проекту \"%s\"' % milestone.project.name,
        u"""Здравствуйте!\nТранш поступил. Статус этапа: \"На реализации\"""", 
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, milestone.project.organization_details.grantee_set.all()),
        fail_silently=False
    )
