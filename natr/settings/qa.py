# -*- coding: utf-8 -*-
from .dev import *

DOCUMENTOLOG_URL = 'http://portal.natd.gov.kz'
DOCUMENTOLOG_CREATE_WSDL = DOCUMENTOLOG_URL + '/ws_kik/workflow/create?wsdl'
DOCUMENTOLOG_EDIT_WSDL = DOCUMENTOLOG_URL + '/ws_kik/workflow/edit?wsdl'
DOCUMENTOLOG_MOVE_WSDL = DOCUMENTOLOG_URL + '/ws_kik/workflow/move?wsdl'
DOCUMENTOLOG_WSDL_USERNAME = 'documentolog'
DOCUMENTOLOG_WSDL_PASSWORD = 'secret'
DOCUMENTOLOG_LOGIN = 'R.Amanzholov@natd.gov.kz'
DOCUMENTOLOG_PASSWORD = 'Qjuehnghj1'
DOCUMENTOLOG_LOGIN_URL = DOCUMENTOLOG_URL + '/user/login'
DOCUMENTOLOG_DOCUMENTS = {
    'plan_monitoring': {
        'title': u'План_мониторинга',
        'uuid': '2a79b458-85bd-4c09-a414-569faae9001a',
    },
}

DOCUMENTOLOG_USER = 'info@documentolog.kz'   # authorize documentolog jsop
DOCUMENTOLOG_TOKEN = '12345678QAZxswe'

CORS_ORIGIN_WHITELIST = (
    'portal.natd.gov.kz',
    '195.12.114.15'
)