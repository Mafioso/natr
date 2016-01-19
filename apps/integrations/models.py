import binascii
import os
import requests
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from . import documentolog
from documents.utils import replace_from_temp


class Token(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(max_length=40, primary_key=True)
    account = models.OneToOneField('auth2.Account', related_name='auth_token')
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user(self):
        return self.account

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class SEDEntity(models.Model):
    ext_doc_id = models.CharField(max_length=255, null=True, unique=True)
    ext_file_url = models.CharField(max_length=255, null=True)
    context_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    context = GenericForeignKey('context_type', 'object_id')


    @classmethod
    def find_by_ext_id(cls, ext_doc_id):
        return SEDEntity.objects.get(ext_doc_id=ext_doc_id)

    @classmethod
    def pin_to_sed(cls, key, instance, **kwargs):
        sed = SEDEntity.objects.create(context=instance)
        sed.ext_doc_id = documentolog.create_document(key, **kwargs)
        sed.save()

    def set_approved(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        self.save()
        self.context.set_approved()
        if not 'ext_file_url' in kwargs:
            return
        data = {
            'login': settings.DOCUMENTOLOG_LOGIN,
            'password': settings.DOCUMENTOLOG_PASSWORD,
        }
        r = requests.post(settings.DOCUMENTOLOG_LOGIN_URL, data=data)
        cookies = r.cookies
        response = requests.get(settings.DOCUMENTOLOG_URL + kwargs['ext_file_url'], cookies=cookies)
        #if response.headers['content-type'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        replace_from_temp(response.content, self.context.attachment.file_path)
