# -*- coding: utf-8 -*-
import os

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
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
        fail_silently=True
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
        fail_silently=True
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
    mail.send(fail_silently=True)

def send_milestone_status_implementation(milestone):
    send_mail(
        u'Смена статуса этапа по проекту \"%s\"' % milestone.project.name,
        u"""Здравствуйте!\nТранш поступил. Статус этапа: \"На реализации\"""", 
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, milestone.project.organization_details.grantee_set.all()),
        fail_silently=True
    )

def send_milestone_status_revision(milestone):
    send_mail(
        u'Смена статуса этапа по проекту \"%s\"' % milestone.project.name,
        u"""Здравствуйте!\nВаш отчет отправлен на доработку. Проверьте кабинет""", 
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, milestone.project.organization_details.grantee_set.all()),
        fail_silently=True
    )

def send_milestone_status_finished(milestone):
    send_mail(
        u'Смена статуса этапа по проекту \"%s\"' % milestone.project.name,
        u"""Здравствуйте!\nЭтап завершен. Сформировано заключение по этапу""", 
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, milestone.project.organization_details.grantee_set.all()),
        fail_silently=True
    )

def send_monitoring_plan_agreed(monitoring):
    def get_monitoring_plan(monitoring):
        table = u'<table style=\'border: 1px solid;\'><thead><tr><th>Мероприятие мониторинга</th><th>Проект</th><th>Начало</th><th>Период</th><th>Завершение</th><th>Форма завершения</th></tr></thead><tbody>%s</tbody></table>' % \
        reduce(lambda x, y: x+u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (y.event_name, y.monitoring.project.name, y.date_start.strftime('%d %m %Y'), y.period, y.date_end.strftime('%d %m %Y'), y.report_type),
                monitoring.todos.all(), u'')
        return table

    mail = EmailMultiAlternatives(
        u'Согласование плана мониторинга по проекту \"%s\"' % monitoring.project.name,
        u"""Здравствуйте!\nВаш план мониторинга был согласован""", 
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, monitoring.project.organization_details.grantee_set.all()) + \
        map(lambda x: x.account.email, monitoring.project.assigned_experts.all()),
    )
    mail.attach_alternative(u'Здравствуйте!\nВаш план мониторинга был согласован\n\n\n'+get_monitoring_plan(monitoring), "text/html")
    mail.send(fail_silently=True)