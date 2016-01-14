# coding: utf-8
import time
from django.conf import settings
from cent.core import generate_token


def get_connection_parameters(user, info=''):
    timestamp = str(int(time.time()))
    user_pk = str(user.pk) if user.is_authenticated() else ""
    token = generate_token(
        settings.CENTRIFUGE_SECRET,
        user_pk,
        timestamp,
        info=info
    )
    return {
        'sockjs_endpoint': settings.CENTRIFUGE_EXTERNAL_ADDRESS + '/connection',
        'ws_endpoint': settings.CENTRIFUGE_EXTERNAL_ADDRESS + '/connection/websocket',
        'user': user_pk,
        'timestamp': timestamp,
        'token': token,
        'info': info
    }


def centrifugo(request):
    params = get_connection_parameters(request.user)
    return dict(
        CENTRIFUGE_SOCKJS_ENDPOINT=params['sockjs_endpoint'],
        CENTRIFUGE_WS_ENDPOINT=params['ws_endpoint'],
        CENTRIFUGE_USER=params['user'],
        CENTRIFUGE_TIMESTAMP=params['timestamp'],
        CENTRIFUGE_TOKEN=params['token'],
        CENTRIFUGE_INFO=params['info']
    )