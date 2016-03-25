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
                map(lambda x: x.account.email, milestone.project.get_grantees())
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
        map(lambda x: x.account.email, milestone.project.get_grantees()),
        fail_silently=True
    )

# TODO: "по отчету ГП уведомления должны приходить .."
def send_milestone_status_revision(milestone):
    print '..here', milestone.project.get_grantees()
    send_mail(
        u'Смена статуса этапа по проекту \"%s\"' % milestone.project.name,
        u"""Здравствуйте!\nВаш отчет отправлен на доработку. Проверьте кабинет""",
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, milestone.project.get_grantees()),
        fail_silently=True
    )

def send_milestone_status_finished(milestone):
    send_mail(
        u'Смена статуса этапа по проекту \"%s\"' % milestone.project.name,
        u"""Здравствуйте!\nЭтап завершен. Сформировано заключение по этапу""",
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, milestone.project.get_grantees()),
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
        map(lambda x: x.account.email, monitoring.project.get_grantees()) + \
        map(lambda x: x.account.email, monitoring.project.assigned_experts.all()),
    )
    mail.attach_alternative(u'Здравствуйте!\nВаш план мониторинга был согласован\n\n\n'+get_monitoring_plan(monitoring), "text/html")
    mail.send(fail_silently=True)

def send_monitoring_plan_gp_approve(monitoring):
    def get_monitoring_plan(monitoring):
        table = u'<table style=\'border: 1px solid;\'><thead><tr><th>Мероприятие мониторинга</th><th>Проект</th><th>Начало</th><th>Период</th><th>Завершение</th><th>Форма завершения</th></tr></thead><tbody>%s</tbody></table>' % \
        reduce(lambda x, y: x+u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (y.event_name, y.monitoring.project.name, y.date_start.strftime('%d %m %Y'), y.period, y.date_end.strftime('%d %m %Y'), y.report_type),
                monitoring.todos.all(), u'')
        return table

    mail_text = u"""Здравствуйте!\nПлан мониторинга был отправлен вам на согласование. \n
            Для утверждения плана перейдите по ссылке: http://178.88.64.87:8000/#/project/%s/monitoring_plan"""%monitoring.project.id

    mail = EmailMultiAlternatives(
        u'Согласование плана мониторинга по проекту \"%s\"' % monitoring.project.name,
        mail_text,
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, monitoring.project.get_grantees()),
    )
    mail.attach_alternative(mail_text+get_monitoring_plan(monitoring), "text/html")
    mail.send(fail_silently=True)

def send_monitoring_plan_approved_by_gp(monitoring):
    def get_monitoring_plan(monitoring):
        table = u'<table style=\'border: 1px solid;\'><thead><tr><th>Мероприятие мониторинга</th><th>Проект</th><th>Начало</th><th>Период</th><th>Завершение</th><th>Форма завершения</th></tr></thead><tbody>%s</tbody></table>' % \
        reduce(lambda x, y: x+u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (y.event_name, y.monitoring.project.name, y.date_start.strftime('%d %m %Y'), y.period, y.date_end.strftime('%d %m %Y'), y.report_type),
                monitoring.todos.all(), u'')
        return table
    mail_text = u"""Здравствуйте!\nПлан мониторинга был согласован грантополучателем. \n
            Для отправки на согласование руководству перейдите по ссылке: http://178.88.64.87:8000/#/projects/edit/%s/monitoring"""%monitoring.project.id
    mail = EmailMultiAlternatives(
        u'Согласование плана мониторинга по проекту \"%s\"' % monitoring.project.name,
        mail_text,
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, monitoring.project.assigned_experts.all())
    )
    mail.attach_alternative(mail_text+get_monitoring_plan(monitoring), "text/html")
    mail.send(fail_silently=True)

def send_monitoring_plan_was_send_to_rework(monitoring, user=None):
    def get_monitoring_plan(monitoring):
        table = u'<table style=\'border: 1px solid;\'><thead><tr><th>Мероприятие мониторинга</th><th>Проект</th><th>Начало</th><th>Период</th><th>Завершение</th><th>Форма завершения</th></tr></thead><tbody>%s</tbody></table>' % \
        reduce(lambda x, y: x+u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (y.event_name, y.monitoring.project.name, y.date_start.strftime('%d %m %Y'), y.period, y.date_end.strftime('%d %m %Y'), y.report_type),
                monitoring.todos.all(), u'')
        return table
    user_info = "План мониторинга был отправлен на доработку"
    if user:
        user_type = ""
        if hasattr(user, 'user'):
            user_type = u"Руководитель"
        elif hasattr(user, 'grantee'):
            user_type = u"Грантополучатель"

        user_info = user_type + u" " +user.get_full_name()+u" отправил(а) план мониторинга на доработку."

    mail_text = u"""Здравствуйте!\n%s. \n
            Для редактирования плана перейдите по ссылке: http://178.88.64.87:8000/#/project/%s/monitoring_plan"""%(user_info, monitoring.project.id)
    mail = EmailMultiAlternatives(
        u'Согласование плана мониторинга по проекту \"%s\"' % monitoring.project.name,
        mail_text,
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, monitoring.project.assigned_experts.all())
    )
    mail.attach_alternative(mail_text+get_monitoring_plan(monitoring), "text/html")
    mail.send(fail_silently=True)

def send_corollary_approved(corollary):
    send_mail(
        u'Заключение по проекту \"%s\" утверждено.' % corollary.project.name,
        u"""Здравствуйте!\nЗаключение по проекту \"%s\" утверждено.""" % corollary.project.name,
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, corollary.project.assigned_experts.all()),
        fail_silently=True
    )

def send_corollary_to_rework(corollary, user=None):
    message_text = u"Заключение, по проекту \"%s\", было отправлено на доработку" % corollary.project.name
    if user:
        user_type = ""
        if hasattr(user, 'user'):
            user_type = u"Руководитель"
        elif hasattr(user, 'grantee'):
            user_type = u"Грантополучатель"

        message_text = user_type + u" " +user.get_full_name()+u" отправил(а) заключение, по проекту \"%s\", на доработку."%corollary.project.name

    send_mail(
        u'Заключение по проекту \"%s\" было отправлено на доработку.' % corollary.project.name,
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, corollary.project.assigned_experts.all()),
        fail_silently=True
    )

def send_project_status_changed(project):
    message_text = u"Здравствуйте. Настоящим письмом уведомляем Вас о %s договора по вашему проекту \"%s\""%(u"завершении" if project.status == 1 else u"расторжении", project.name)

    send_mail(
        u"%s договора"%(u"Завершение" if project.status == 1 else u"Расторжение"),
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, project.get_grantees()),
        fail_silently=True
    )

def send_grantee_approve_email(monitoring_plan):
    message_text = u"Здравствуйте! По Вашему проекту \"%s\" поступил план мониторинга."%monitoring_plan.project.name

    send_mail(
        u"%s договора"%(u"Завершение" if monitoring_plan.project.status == 1 else u"Расторжение"),
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, monitoring_plan.project.get_grantees()),
        fail_silently=True
    )