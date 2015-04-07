#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime
from django.db import models

from core.models import Brand
from services_media.models import AdwordsConnection

from oauth2client.django_orm import CredentialsField

from south.modelsinspector import add_introspection_rules



class AdwordsAccount(models.Model):

    """
    AdwordsAccount
    =========

    AdwordsAccount is a model to store main info about adwords account.

    e.g. 
    AdwordsAccount: 
    Chevrolet Brasil
    485-332-8383

    """

    adwords_connection = models.ForeignKey(AdwordsConnection, verbose_name=u'Conexão do Adwords', blank=False)
    brand = models.ForeignKey(Brand, verbose_name=u'Marca')
    client_id = models.CharField(verbose_name=u'ID do Cliente', max_length=255, blank=False, unique=True)
    first_load_ad = models.BooleanField(verbose_name=u'Primeiro Load Ad Levek', default=False, blank=False)
    first_load_keyword = models.BooleanField(verbose_name=u'Primeiro Load KW Level', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.adwords_connection.email

    class Meta:
        ordering = [u'adwords_connection']
        verbose_name = u'Conta do Adwords'
        verbose_name_plural = u'Contas do Adwords'