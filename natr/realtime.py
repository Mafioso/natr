from contextlib import contextmanager
from adjacent import Client
from rest_framework.utils.encoders import JSONEncoder


centrifugo_client = Client(json_encoder=JSONEncoder)


@contextmanager
def send_in_bulk():
    yield centrifugo_client
    centrifugo_client.send()