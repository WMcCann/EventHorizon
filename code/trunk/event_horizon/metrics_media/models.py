#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime
from django.db import models

from core.models import Person, APIError
from media.models import AdwordsAccount


class AdwordsKeyword(models.Model):

    """
    AdwordsKeyword
    =========

    AdwordsKeyword is a model to store all adwords keyword metrics.

    """

    adwords_account = models.ForeignKey(AdwordsAccount, verbose_name=u'Conta do Adwords', blank=False)
    day = models.DateField(verbose_name=u'Data', blank=False, null=False)
    keyword_status = models.CharField(verbose_name=u'Status Keyword', max_length=255, blank=False)
    keyword_id = models.CharField(verbose_name=u'ID Keyword', max_length=255, blank=False)
    keyword = models.CharField(verbose_name=u'Keyword', max_length=255, blank=False)
    campaign_status = models.CharField(verbose_name=u'Status Campanha', max_length=255, blank=False)
    campaign_id = models.CharField(verbose_name=u'ID Campanha', max_length=255, blank=False)
    campaign = models.CharField(verbose_name=u'Campanha', max_length=255, blank=False)
    adgroup_status = models.CharField(verbose_name=u'Status AdGroup', max_length=255, blank=False)
    adgroup_id = models.CharField(verbose_name=u'ID AdGroup', max_length=255, blank=False)
    adgroup = models.CharField(verbose_name=u'AdGroup', max_length=255, blank=False)
    placement_url = models.CharField(verbose_name=u'Placement Url', max_length=255, blank=False)
    max_cpc = models.BigIntegerField(verbose_name=u'Máx CPC', default=0, blank=False)
    clicks = models.BigIntegerField(verbose_name=u'Cliques', default=0, blank=False)
    impressions = models.BigIntegerField(verbose_name=u'Impressões', default=0, blank=False)
    cost = models.BigIntegerField(verbose_name=u'Custo', default=0, blank=False)
    search_impressions_share = models.CharField(verbose_name=u'Share Impressões Search', max_length=255, blank=False)
    search_exact_match = models.CharField(verbose_name=u'Search Exact Match', max_length=255, blank=False)
    avg_position = models.FloatField(verbose_name=u'AVG Position', default=0, blank=False)
    week = models.DateField(verbose_name=u'Semana', blank=False, null=False)


    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)

    def __unicode__(self):
        return self.adwords_account

    class Meta:
        ordering = [u'-created_at']
        verbose_name = u'Keyword do Adwords'
        verbose_name_plural = u'Keywords do Adwords'


class AdwordsAd(models.Model):

    """
    AdwordsAd
    =========

    AdwordsAd is a model to store all adwords ads metrics.

    """

    adwords_account = models.ForeignKey(AdwordsAccount, verbose_name=u'Conta do Adwords', blank=False)
    day = models.DateField(verbose_name=u'Data', blank=False, null=False)
    ad_status = models.CharField(verbose_name=u'Status Ad', max_length=255, blank=False)
    ad_id = models.CharField(verbose_name=u'ID Ad', max_length=255, blank=False)
    ad = models.CharField(verbose_name=u'Ad', max_length=255, blank=False)
    description_1 = models.CharField(verbose_name=u'Descrição 1', max_length=255, blank=False)
    description_2 = models.CharField(verbose_name=u'Descrição 2', max_length=255, blank=False)
    display_url = models.CharField(verbose_name=u'URL Visualização', max_length=255, blank=False)
    url = models.CharField(verbose_name=u'URL', max_length=255, blank=False)

    campaign_status = models.CharField(verbose_name=u'Status Campanha', max_length=255, blank=False)
    campaign_id = models.CharField(verbose_name=u'ID Campanha', max_length=255, blank=False)
    campaign = models.CharField(verbose_name=u'Campanha', max_length=255, blank=False)
    adgroup_status = models.CharField(verbose_name=u'Status AdGroup', max_length=255, blank=False)
    adgroup_id = models.CharField(verbose_name=u'ID AdGroup', max_length=255, blank=False)
    adgroup = models.CharField(verbose_name=u'AdGroup', max_length=255, blank=False)
    clicks = models.BigIntegerField(verbose_name=u'Cliques', default=0, blank=False)
    impressions = models.BigIntegerField(verbose_name=u'Impressões', default=0, blank=False)
    cost = models.BigIntegerField(verbose_name=u'Custo', default=0, blank=False)
    

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)

    def __unicode__(self):
        return self.adwords_account

    class Meta:
        ordering = [u'-created_at']
        verbose_name = u'Keyword do Adwords'
        verbose_name_plural = u'Keywords do Adwords'