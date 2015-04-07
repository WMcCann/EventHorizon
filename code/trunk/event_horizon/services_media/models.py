#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings

from datetime import datetime
from django.db import models

from oauth2client.django_orm import CredentialsField

from south.modelsinspector import add_introspection_rules


# instrospection rules for south
add_introspection_rules([], ["^oauth2client\.django_orm\.CredentialsField"])
class AdwordsConnection(models.Model):

    """
    AdwordsConnection
    =========

    AdwordsConnection is a model to store connection data from adwords.

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
        verbose_name = u'Conexão do Adwords'
        verbose_name_plural = u'Conexões do Adwords'


    def save(self, *args, **kwargs):
        super(AdwordsConnection, self).save(*args, **kwargs)
