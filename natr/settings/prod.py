from .common import *


MEDIA_ROOT = '/uploads'
NGINX_TMP_UPLOAD_ROOT = os.path.join(MEDIA_ROOT, 'tmp')
HOST = '178.88.64.87'
DOCKER_HOST = '178.88.64.87'
CENTRIFUGO_PORT = os.getenv('CENTRIFUGO_PORT_8001_TCP_PORT', 8001)
CENTRIFUGE_EXTERNAL_ADDRESS = 'http://{}:{}'.format(DOCKER_HOST, CENTRIFUGO_PORT)