from django.conf import settings
from chat.models import prepare_channel


def main(request):
    return dict(
        CHAT_CHANNEL=prepare_channel(request.user.pk)
    )