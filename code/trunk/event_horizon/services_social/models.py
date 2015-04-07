#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings

from datetime import datetime
from django.db import models

from oauth2client.django_orm import CredentialsField

from south.modelsinspector import add_introspection_rules


class FacebookConnection(models.Model):

    """
    FacebookConnection
    =========

    FacebookConnection is a model to store connection data from facebook.

    """

    conn_id = models.CharField(verbose_name=u'ID da conexão (ID Perfil)', max_length=255, blank=False, unique=True)
    name = models.CharField(verbose_name=u'Nome da conexão (Nome do Perfil)', max_length=255, blank=False)
    access_token = models.TextField(verbose_name=u'Token de acesso', blank=False)
    expires = models.DateTimeField(verbose_name=u'Expiração', blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Conexão do Facebook'
        verbose_name_plural = u'Conexões do Facebook'


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(FacebookConnection, self).save(*args, **kwargs)

    @classmethod
    def renew_client(cls, fbc):
        # get some access_token
        new_fbc = FacebookConnection.objects.filter(expires__gt=datetime.now(), deleted=False).exclude(id__exact=fbc.id)[0]

        return new_fbc, new_fbc.access_token


class TwitterConnection(models.Model):

    """
    TwitterConnection
    =========

    TwitterConnection is a model to store connection data from twitter.

    """

    name = models.CharField(verbose_name=u'Nome da conexão', max_length=255, blank=False)
    access_token = models.TextField(verbose_name=u'Token de acesso', blank=False)
    access_token_secret = models.TextField(verbose_name=u'Token de acesso secreto', blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Conexão do Twitter'
        verbose_name_plural = u'Conexões do Twitter'


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(TwitterConnection, self).save(*args, **kwargs)


# instrospection rules for south
add_introspection_rules([], ["^oauth2client\.django_orm\.CredentialsField"])
class YoutubeConnection(models.Model):

    """
    YoutubeConnection
    =========

    YoutubeConnection is a model to store connection data from youtube.

    """

    email = models.EmailField(verbose_name=u'E-mail', blank=False, primary_key=True)
    credential = CredentialsField()

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.email

    class Meta:
        ordering = [u'email']
        verbose_name = u'Conexão do Youtube'
        verbose_name_plural = u'Conexões do Youtube'


    def save(self, *args, **kwargs):
        super(YoutubeConnection, self).save(*args, **kwargs)