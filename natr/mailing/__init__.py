# -*- coding: utf-8 -*-
import os

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from documents.utils import DocumentPrint
import mimetypes

def get_user_info(user):
    if not user:
        return None

    if hasattr(user, 'user'):
        if user.user.is_director():
            return u"Директор "+user.get_full_name()
        elif user.user.is_manager():
            return u"Руководитель "+user.get_full_name()
        elif user.user.is_expert():
            return u"Эксперт "+user.get_full_name()
        elif user.user.is_risk_expert():
            return u"Риск эксперт "+user.get_full_name()
        elif user.user.is_independent_expert():
            return u"Независимый эксперт "+user.get_full_name()
        else:
            return NatrGroup.EXPERT
    elif hasattr(user, 'grantee'):
        return u"Грантополучатель "+user.get_full_name()

    return user.get_full_name()

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
                u"""Здравствуйте!\nНачался этап №%s по вашему проекту \"%s\". Просим ознакомится с памяткой""" %(milestone.number, milestone.project.name),
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

def send_monitoring_plan_gp_approve(monitoring, user=None):
    def get_monitoring_plan(monitoring):
        table = u'<br /><br /><table style=\'border: 1px solid;\'><thead><tr><th>Мероприятие мониторинга</th><th>Проект</th><th>Начало</th><th>Период</th><th>Завершение</th><th>Форма завершения</th></tr></thead><tbody>%s</tbody></table>' % \
        reduce(lambda x, y: x+u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (y.event_name, y.monitoring.project.name, y.date_start.strftime('%d %m %Y') if y.date_start else "", y.period, y.date_end.strftime('%d %m %Y') if y.date_end else "", y.report_type),
                monitoring.todos.all(), u'')
        return table

    title = u'План мониторинга "%s"'%(monitoring.project.organization_details.name)
    mail_text = u"Добрый день!\n" + (get_user_info(user) + u" отправил(а) план мониторинга на согласование." if user else u"План мониторинга был отправлен вам на согласование." )

    mail = EmailMultiAlternatives(
        title,
        mail_text,
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, monitoring.project.get_grantees()),
    )
    mail.attach_alternative(mail_text+get_monitoring_plan(monitoring), "text/html")
    mail.send(fail_silently=True)

#TODO
def send_monitoring_plan_manager_approve(monitoring, user=None):
    def get_monitoring_plan(monitoring):
        table = u'<br /><br /><table style=\'border: 1px solid;\'><thead><tr><th>Мероприятие мониторинга</th><th>Проект</th><th>Начало</th><th>Период</th><th>Завершение</th><th>Форма завершения</th></tr></thead><tbody>%s</tbody></table>' % \
        reduce(lambda x, y: x+u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (y.event_name, y.monitoring.project.name, y.date_start.strftime('%d %m %Y') if y.date_start else "", y.period, y.date_end.strftime('%d %m %Y') if y.date_end else "", y.report_type),
                monitoring.todos.all(), u'')
        return table

    title = u'План мониторинга "%s"'%(monitoring.project.organization_details.name)
    mail_text = u"Добрый день! \n" + (get_user_info(user) + u" отправил(а) план мониторинга на согласование." if user else u"План мониторинга был отправлен вам на согласование." )
    managers = []
    for a in auth_models.Account.objects.all():
        if a.is_manager():
            managers.append(a.email)

    mail = EmailMultiAlternatives(
        title,
        mail_text,
        settings.DEFAULT_FROM_EMAIL,
        managers
    )
    mail.attach_alternative(mail_text+get_monitoring_plan(monitoring), "text/html")
    mail.send(fail_silently=True)

#TODO
def send_monitoring_plan_director_approve(monitoring, user=None):
    def get_monitoring_plan(monitoring):
        table = u'<br /><br /><table style=\'border: 1px solid;\'><thead><tr><th>Мероприятие мониторинга</th><th>Проект</th><th>Начало</th><th>Период</th><th>Завершение</th><th>Форма завершения</th></tr></thead><tbody>%s</tbody></table>' % \
        reduce(lambda x, y: x+u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (y.event_name, y.monitoring.project.name, y.date_start.strftime('%d %m %Y') if y.date_start else "", y.period, y.date_end.strftime('%d %m %Y') if y.date_end else "", y.report_type),
                monitoring.todos.all(), u'')
        return table

    title = u'План мониторинга "%s"'%(monitoring.project.organization_details.name)
    mail_text = u"Добрый день! \n" + (get_user_info(user) + u" отправил(а) план мониторинга на утверждение." if user else u"План мониторинга был отправлен вам на утверждение." )
    directors = []
    for a in auth_models.Account.objects.all():
        if a.is_director():
            directors.append(a.email)

    mail = EmailMultiAlternatives(
        title,
        mail_text,
        settings.DEFAULT_FROM_EMAIL,
        directors
    )
    mail.attach_alternative(mail_text+get_monitoring_plan(monitoring), "text/html")
    mail.send(fail_silently=True)

def send_monitoring_plan_approved(monitoring, user=None):
    def get_monitoring_plan(monitoring):
        table = u'<br /><br /><table style=\'border: 1px solid;\'><thead><tr><th>Мероприятие мониторинга</th><th>Проект</th><th>Начало</th><th>Период</th><th>Завершение</th><th>Форма завершения</th></tr></thead><tbody>%s</tbody></table>' % \
        reduce(lambda x, y: x+u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (y.event_name, y.monitoring.project.name, y.date_start.strftime('%d %m %Y') if y.date_start else "", y.period, y.date_end.strftime('%d %m %Y') if y.date_end else "", y.report_type),
                monitoring.todos.all(), u'')
        return table

    title = u'План мониторинга "%s"'%(monitoring.project.organization_details.name)
    mail_text = u"Добрый день! \n" + (get_user_info(user) + u" утвердил план мониторинга" if user else u"Директор утвердил план мониторинга." )

    mail = EmailMultiAlternatives(
        title,
        mail_text,
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, monitoring.project.assigned_experts.all()) + map(lambda x: x.account.email, monitoring.project.get_grantees())
    )
    mail.attach_alternative(mail_text+get_monitoring_plan(monitoring), "text/html")
    mail.send(fail_silently=True)

def send_monitoring_plan_on_rework(monitoring, user=None):
    def get_monitoring_plan(monitoring):
        table = u'<br /><br /><table style=\'border: 1px solid;\'><thead><tr><th>Мероприятие мониторинга</th><th>Проект</th><th>Начало</th><th>Период</th><th>Завершение</th><th>Форма завершения</th></tr></thead><tbody>%s</tbody></table>' % \
        reduce(lambda x, y: x+u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (y.event_name, y.monitoring.project.name, y.date_start.strftime('%d %m %Y') if y.date_start else "", y.period, y.date_end.strftime('%d %m %Y') if y.date_end else "", y.report_type),
                monitoring.todos.all(), u'')
        return table

    title = u'План мониторинга "%s"'%(monitoring.project.organization_details.name)
    mail_text = u"Добрый день! \n" + (get_user_info(user) + u" отправил(а) план мониторинга на доработку." if user else u"План мониторинга был отправлен вам на доработку." )

    mail = EmailMultiAlternatives(
        title,
        mail_text,
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, monitoring.project.assigned_experts.all())
    )
    mail.attach_alternative(mail_text+get_monitoring_plan(monitoring), "text/html")
    mail.send(fail_silently=True)

def send_corollary_approved(corollary, user=None):
    send_mail(
        u'Заключение по проекту \"%s\" утверждено.' % corollary.project.name,
        u"""Здравствуйте!\n %s утвердил заключение по проекту \"%s\".""" % (user.get_full_name(), corollary.project.name),
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, corollary.project.assigned_experts.all()),
        fail_silently=True
    )

def send_corollary_to_rework(corollary, user=None, comment=None):
    if comment:
        comment = u"Комментарий: \n%s"%comment.comment_text
    else:
        comment = u""

    message_text = u"Заключение, по проекту \"%s\", было отправлено на доработку. %s" % (corollary.project.name, comment)

    if user:
        user_type = ""
        if hasattr(user, 'user'):
            user_type = u"Руководитель"
        elif hasattr(user, 'grantee'):
            user_type = u"Грантополучатель"

        message_text = user_type + u" " +user.get_full_name()+u" отправил(а) заключение, по проекту \"%s\", на доработку. %s"%(corollary.project.name, comment)

    send_mail(
        u'Заключение по проекту \"%s\" было отправлено на доработку.' % corollary.project.name,
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, corollary.project.assigned_experts.all()),
        fail_silently=True
    )

def send_corollary_to_approve(corollary, user=None):
    message_text = u"Заключение, по проекту \"%s\", было отправлено на доработку" % corollary.project.name
    if user:
        message_text = user.get_full_name()+u" отправил(а) заключение, по проекту \"%s\", на согласование руководителем."%corollary.project.name

    send_mail(
        u'Заключение по проекту \"%s\" было отправлено на согласование.' % corollary.project.name,
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
        u"План мониторинга",
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, monitoring_plan.project.get_grantees()),
        fail_silently=True
    )

def send_chat_activity(text_line, from_account):
    from_type = ""
    to_accounts = []

    if from_account:
        if hasattr(from_account, 'user'):
            from_type = u"Эксперт"
            to_type = u"грантополучатель"
            to_accounts = map(lambda x: x.account.email, text_line.project.get_grantees())
        elif hasattr(from_account, 'grantee'):
            from_type = u"Грантополучатель"
            to_type = u"эксперт"
            to_accounts = map(lambda x: x.account.email, text_line.project.assigned_experts.all())

    title = u"Новое сообщение в ИСЭМ"
    message_text = u"""Уважаемый %s! \n%s %s отправил вам сообщение: \n%s \n
                    Ссылка для входа в кабинет: http://178.88.64.87:8000"""%(to_type,
                                                                             from_type, 
                                                                             from_account.get_full_name(), 
                                                                             text_line.line)
    send_mail(
        title,
        message_text,
        settings.DEFAULT_FROM_EMAIL,
        to_accounts,
        fail_silently = True
    )

def send_corollary_dir_check(corollary, user):
    send_mail(
        u'Заключение по проекту \"%s\" согласовано руководителем, и отправлено на утверждение.' % corollary.project.name,
        u"""Здравствуйте!\nЗаключение по проекту \"%s\" согласовано руководителем, %s, и отправлено на утверждение.""" % (corollary.project.name, user.get_full_name()),
        settings.DEFAULT_FROM_EMAIL,
        map(lambda x: x.account.email, corollary.project.assigned_experts.all()),
        fail_silently=True
    )

def send_milestone_status_payment(report):
    mail = EmailMessage(
                u'Отправлен отчет на проверку по проекту \"%s\"' % report.project.name,
                u"""Здравствуйте! Отправлен отчет, по проекту \"%s\", на проверку """ %(report.project.name),
                settings.DEFAULT_FROM_EMAIL,
                ['info@natd.gov.kz']
            )

    for cover_letter in report.cover_letter_atch.all():
        with open(cover_letter.file_path, "rb") as f:
            mail.attach(u"Soprovoditelnoje pismo.docx", f.read(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    
    try:
        _file, filename = DocumentPrint(object=report).generate_docx()
        mail.attach(u"Otchet.docx", _file.read(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except:
        pass

    mail.send(fail_silently=True)


def send_announcement_with_official_email(notification):
    notif_params = notification.prepare_msg()
    official_email = notification.context

    mail = EmailMessage(
                u'Уведомление официальным письмом \"%s\"' % official_email.reg_number,
                u"""Здравствуйте! Получено уведомление, по проекту \"%s\", с коментарием: \"%s\". 
                Официальное письмо во вложений к этому письму. 
                Регистрационный номер письма - \"%s\", дата регистрации - \"%s\.""" %(
                    notif_params['project_name'], notif_params['text'], official_email.reg_number, 
                    official_email.reg_date),
                settings.DEFAULT_FROM_EMAIL,
                ['info@natd.gov.kz']
            )

    for attachment_data in official_email.attachments.all():
        with open(attachment_data.file_path, "rb") as f:
            mail.attach(attachment_data.name, f.read(), mimetypes.guess_type('f%s' % attachment_data.ext)[0])

    mail.send(fail_silently=True)

def send_monitoring_todo_days_left(mtodo, days):
    for grantee in mtodo.project.assigned_grantees.all():
        send_mail(
            u'Напоминанием о запланированном мероприятии, по проекту %s'%(mtodo.project.name),
            u"""Здравствуйте, {name}!

            По проекту {project_name},
            с {date_start} по {date_end} (до завершения остается {days} дней)
            запланировано мероприятие: {event_name}.
            Форма завершения: {report_type}

            Ссылка на План Мониторинга: {host_address}/#/project/{project_id}/monitoring_plan """.format(**{
                'name': grantee.account.get_full_name(),
                'project_name': mtodo.project.name,
                'project_id': mtodo.project.id,
                'date_start': mtodo.date_start and mtodo.date_start.strftime("%d.%m.%Y") or '?',
                'date_end': mtodo.date_end and mtodo.date_end.strftime("%d.%m.%Y") or '?',
                'event_name': mtodo.event_name,
                'report_type': mtodo.report_type,
                'days': days,
                'host_address': settings.DOCKER_APP_ADDRESS
            }),
            settings.DEFAULT_FROM_EMAIL,
            [grantee.account.email],
            fail_silently=False
        )   

    for expert in mtodo.project.assigned_experts.all():
        send_mail(
            u'Напоминанием о запланированном мероприятии, по проекту %s'%(mtodo.project.name),
            u"""Здравствуйте, {name}!

            По проекту {project_name},
            с {date_start} по {date_end} (до завершения остается {days} дней)
            запланировано мероприятие: {event_name}.
            Форма завершения: {report_type}

            Ссылка на План Мониторинга: {host_address}/#/project/{project_id}/monitoring_plan """.format(**{
                'name': expert.account.get_full_name(),
                'project_name': mtodo.project.name,
                'project_id': mtodo.project.id,
                'date_start': mtodo.date_start and mtodo.date_start.strftime("%d.%m.%Y") or '?',
                'date_end': mtodo.date_end and mtodo.date_end.strftime("%d.%m.%Y") or '?',
                'event_name': mtodo.event_name,
                'report_type': mtodo.report_type,
                'days': days,
                'host_address': settings.DOCKER_APP_ADDRESS
            }),
            settings.DEFAULT_FROM_EMAIL,
            [expert.account.email],
            fail_silently=False
        )