# -*- coding: utf-8 -*-

"""
Django settings for natr project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys



def FileSettings(path):
    path = os.path.expanduser(path)

    class Holder(object):

        def __init__(self, *args, **kwargs):
            mod = imp.new_module('natr.local')
            mod.__file__ = path

            try:
                execfile(path, mod.__dict__)
            except IOError, e:
                print("Notice: Unable to load configuration file %s (%s), "
                      "using default settings\n\n" % (path, e.strerror))

            for name, value in uppercase_attributes(mod).items():
                if hasattr(self, name):
                    original_value = getattr(self, name)
                    if isinstance(original_value, (tuple, list)):
                        if value.startswith('+'):
                            value = tuple(original_value) + tuple(value[1:].split(','))
                        else:
                            value = tuple([value])
                setattr(self, name, value)

    return Holder


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def rel(*x):
    return os.path.join(os.path.abspath(BASE_DIR), *x)

sys.path.insert(0, rel('apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gw^bd_dd11*_c%89vk3p7bmn6jubn6o_(@8jjz^*2ixfy!ag!#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

APPS = (
    'natr',
    'dummy',
    'projects',
    'documents',
    'grantee',
    'journals',
    'resources',
    'auth2',
    'notifications'
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'rest_framework_swagger',
    'test_without_migrations'
) + APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'natr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [rel('templates',), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'adjacent.context_processors.main',
                'notifications.context_processors.main'
            ],
        },
    },
]

WSGI_APPLICATION = 'natr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': rel('natr_dev.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EXCEL_REPORTS_DIR = rel(BASE_DIR, 'excel_reports')
DOCX_TEMPLATES_DIR = rel(BASE_DIR, 'docx_templates')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'
MEDIA_URL_NO_TRAILING_SLASH = '/uploads'
STATIC_ROOT = rel('..', 'static')
MEDIA_ROOT = '/uploads'

NGINX_TMP_UPLOAD_ROOT = os.path.join(MEDIA_ROOT, 'tmp')

STATICFILES_DIRS = (
    rel('static'),
)

LOCALE_PATHS = (
    rel('locale'),
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'natr.rest_framework.authentication.DummyAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'PAGE_SIZE': 10,
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}

ADMINS = (('Rustem', 'r.kamun@gmail.com'),
          ('Yernar', 'mailubai@gmail.com'),)


AUTH_USER_MODEL = 'auth2.Account'
LOGIN_REDIRECT_URL = 'home'
# celery conf
BROKER_HOST = os.getenv('RABBITMQ_PORT_5672_TCP_ADDR', '127.0.0.1')
BROKER_PORT = os.getenv('RABBITMQ_PORT_5672_TCP_PORT', 5672)
BROKER_USER_PASSWORD = os.getenv('RABBITMQ_ENV_RABBITMQ_USER_PASSWD', 'guest:guest')
BROKER_VHOST = os.getenv('RABBITMQ_ENV_RABBITMQ_DEFAULT_VHOST', '/')

BROKER_URL = 'amqp://{user_passwd}@{host}/{vhost}'.format(**{
    'user_passwd': BROKER_USER_PASSWORD,
    'host': BROKER_HOST,
    'port': BROKER_PORT,
    'vhost': BROKER_VHOST
})


CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

SHELL_PLUS_PRE_IMPORTS = (
    'projects.factories',
    'documents.factories',
    ('faker', '*'),
    ('resources.project', '*'),
    ('resources.serializers', '*'),
    ('documents.serializers', '*'),
    ('grantee.serializers', '*'),
       
)

KZT = 'KZT'
USD = 'USD'
CURRENCIES = (KZT, USD)

NOTIFICATION_CHANNEL = 'notification'

CENTRIFUGO_HOST = os.getenv('CENTRIFUGO_PORT_8001_TCP_ADDR', 'centrifugo.natr.kz')
CENTRIFUGO_PORT = os.getenv('CENTRIFUGO_PORT_8001_TCP_PORT', 8001)
CENTRIFUGE_ADDRESS = 'http://{}:{}'.format(CENTRIFUGO_HOST, CENTRIFUGO_PORT)
CENTRIFUGE_SECRET = 'secret'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.yandex.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'test.ko@almasales.com'
EMAIL_HOST_PASSWORD = '123qweasd'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# DEFAULT_TO_EMAIL = 'to email'

DOCUMENTOLOG_URL = 'http://kik.doc24.kz'
DOCUMENTOLOG_CREATE_WSDL = DOCUMENTOLOG_URL + '/ws_kik/workflow/create?wsdl'
DOCUMENTOLOG_EDIT_WSDL = DOCUMENTOLOG_URL + '/ws_kik/workflow/edit?wsdl'
DOCUMENTOLOG_MOVE_WSDL = DOCUMENTOLOG_URL + '/ws_kik/workflow/move?wsdl'
DOCUMENTOLOG_WSDL_USERNAME = 'documentolog'
DOCUMENTOLOG_WSDL_PASSWORD = 'secret'
DOCUMENTOLOG_DOCUMENTS = {
    'plan_monitoring': {
        'title': u'План_мониторинга',
        'uuid': '430c493c-dabf-43dc-9e95-568cf65501f4',
    },
}