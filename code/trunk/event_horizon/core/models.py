#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models


class Country(models.Model):

    """
    Country (GEO)
    =========

    Country is a model to store all country information.

    e.g. 
    Country: Brazil

    """

    name = models.CharField(verbose_name=u'Nome', max_length=255, blank=False)
    mnemonic = models.CharField(verbose_name=u'Mnemônica', max_length=255, blank=True, null=True)
    cod_sap = models.CharField(verbose_name=u'Cód. SAP', max_length=2, blank=True, null=True)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'País'
        verbose_name_plural = u'Países'


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.mnemonic = self.mnemonic.upper()
        super(Country, self).save(*args, **kwargs)


class Company(models.Model):

    """
    Company
    =========

    Company is a model to store all company information.

    e.g. 
    Company: WMcCann

    """

    name = models.CharField(verbose_name=u'Nome', max_length=255, blank=False)
    mnemonic = models.CharField(verbose_name=u'Mnemônica', max_length=255, blank=True, null=True)
    id_sap = models.IntegerField(verbose_name=u'ID SAP', blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name=u'País')
    active = models.BooleanField(verbose_name=u'Ativo', default=True, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Companhia'
        verbose_name_plural = u'Companhias'


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.mnemonic = self.mnemonic.upper()
        super(Company, self).save(*args, **kwargs)



class Advertiser(models.Model):

    """
    Advertiser
    =========

    Advertiser is a model to store all advertiser information.
    Be careful with our abstracted vision about market and our clients. It'll be defined in company_owner field.

    e.g. 
    Advertiser: GM

    """

    name = models.CharField(verbose_name=u'Nome', max_length=255, blank=False)
    mnemonic = models.CharField(verbose_name=u'Mnemônica', max_length=255, blank=True, null=True)
    id_sap = models.IntegerField(verbose_name=u'ID SAP', blank=True, null=True)
    company_owner = models.ForeignKey(Company, verbose_name=u'Companhia detentora', blank=True, null=True)
    abbreviation = models.CharField(verbose_name=u'Abreviação', max_length=255, blank=True, null=True)
    active = models.BooleanField(verbose_name=u'Ativo', default=True, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Advertiser'
        verbose_name_plural = u'Advertisers'


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.mnemonic = self.mnemonic.upper()
        self.abbreviation = self.abbreviation.upper()
        super(Advertiser, self).save(*args, **kwargs)


class Sector(models.Model):

    """
    Sector
    =========

    Sector is a model to store all economic sector information.

    e.g. 
    Sector: Agriculture

    """

    name = models.CharField(verbose_name=u'Nome', max_length=255, blank=False)
    mnemonic = models.CharField(verbose_name=u'Mnemônica', max_length=255, blank=True, null=True)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Setor'
        verbose_name_plural = u'Setores'


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.mnemonic = self.mnemonic.upper()
        super(Sector, self).save(*args, **kwargs)


class Category(models.Model):

    """
    Category
    =========

    Category is a model to store all economic sector's categories information.

    e.g. 
    Category: Pet Accessories

    """

    name = models.CharField(verbose_name=u'Nome', max_length=255, blank=False)
    mnemonic = models.CharField(verbose_name=u'Mnemônica', max_length=255, blank=True, null=True)
    sector = models.ForeignKey(Sector, verbose_name=u'Setor')

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Categoria'
        verbose_name_plural = u'Categorias'


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.mnemonic = self.mnemonic.upper()
        super(Category, self).save(*args, **kwargs)


class Brand(models.Model):

    """
    Brand
    =========

    Brand is a model to store all brand information.

    e.g. 
    Brand: Chevrolet

    """

    name = models.CharField(verbose_name=u'Nome', max_length=255, blank=False)
    mnemonic = models.CharField(verbose_name=u'Mnemônica', max_length=255, blank=True, null=True)
    id_sap = models.IntegerField(verbose_name=u'ID SAP', blank=True, null=True)
    advertiser = models.ForeignKey(Advertiser, verbose_name=u'Advertiser')
    category = models.ForeignKey(Category, verbose_name=u'Categoria')
    country = models.ForeignKey(Country, verbose_name=u'País')

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Marca'
        verbose_name_plural = u'Marcas'


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.mnemonic = self.mnemonic.upper()
        super(Brand, self).save(*args, **kwargs)


class Campaign(models.Model):

    """
    Campaign
    =========

    Campaign is a model to store all campaign information.

    e.g. 
    Campaign: Find New Roads

    """

    name = models.CharField(verbose_name=u'Nome', max_length=255, blank=False)
    mnemonic = models.CharField(verbose_name=u'Mnemônica', max_length=255, blank=True, null=True)
    id_sap = models.IntegerField(verbose_name=u'ID SAP', blank=True, null=True)
    brand = models.ForeignKey(Brand, verbose_name=u'Marca')
    initiation_date = models.DateTimeField(verbose_name=u'Data de início', blank=False)
    ending_date = models.DateTimeField(verbose_name=u'Data de término', blank=False)
    active = models.BooleanField(verbose_name=u'Ativo', default=True, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Campanha'
        verbose_name_plural = u'Campanhas'


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.mnemonic = self.mnemonic.upper()
        super(Campaign, self).save(*args, **kwargs)


class Person(models.Model):

    """
    Person
    =========

    Person is a model to centralize all person information.
    It's a vision about our CRM and all kind of information about a person is centralized here.
    Facebook profile, Twitter profile and so on, all of this will be plugged here.

    e.g. 
    Person: Johann Vivot

    """

    name = models.CharField(verbose_name=u'Nome', max_length=255, blank=True, null=True)
    gender = models.CharField(verbose_name=u'Sexo', max_length=255, blank=True, null=True)
    email = models.EmailField(verbose_name=u'E-mail', max_length=254, blank=True, null=True)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Pessoa'
        verbose_name_plural = u'Pessoas'


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.gender = self.gender.upper()
        self.email = self.email.upper()
        super(Person, self).save(*args, **kwargs)


class APIError(models.Model):

    """
    APIError
    =========

    APIError is a model to centralize all unexpected information that were come from APIs.

    e.g. 
    APIError:
    metrics_social
    FacebookMessage
    KeyError: u'message'
    {
        u 'story': u '"Olá Madson, para que possamos..." on Madson Alves's post on Chevrolet Brasil's wall.',
        u 'from': {
            u 'category': u 'Automobiles and parts',
            u 'name': u 'Chevrolet Brasil',
            u 'id': u '117750778311686'
        },
        u 'privacy': {
            u 'value': u ''
        },
        u 'updated_time': u '2013-08-06T12:07:28+0000',
        u 'application': {
            u 'name': u 'Facebook for Every Phone',
            u 'id': u '139682082719810'
        },
        u 'story_tags': {
            u '38': [{
                u 'length': 12,
                u 'offset': 38,
                u 'type': u 'user',
                u 'id': u '100004003127528',
                u 'name': u 'Madson Alves'
            }]
        },
        u 'created_time': u '2013-08-06T12:07:28+0000',
        u 'type': u 'status',
        u 'id': u '117750778311686_504330702987023'
    }

    """

    app_name = models.CharField(verbose_name=u'Nome da App', max_length=255, blank=False)
    model_name = models.CharField(verbose_name=u'Nome do Modelo', max_length=255, blank=False)
    error = models.TextField(verbose_name=u'Erro', blank=False)
    response = models.TextField(verbose_name=u'Resposta', blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.error

    class Meta:
        ordering = [u'error']
        verbose_name = u'Erro de API'
        verbose_name_plural = u'Erros de APIs'


class APIPagination(models.Model):

    """
    APIPagination
    =========

    APIPagination is a model to store pagination from APIs.

    e.g. 
    APIPagination:
    metrics_social
    FacebookComments
    /117750778311686_509232919163468/comments
    MjY3

    """

    app_name = models.CharField(verbose_name=u'Nome da App', max_length=255, blank=False)
    model_name = models.CharField(verbose_name=u'Nome do Modelo', max_length=255, blank=False)
    path = models.CharField(verbose_name=u'Path', max_length=255, blank=False)
    offset = models.CharField(verbose_name=u'Offset', max_length=255, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.path

    class Meta:
        unique_together = ('app_name', 'model_name', 'path',)
        ordering = [u'model_name']
        verbose_name = u'Paginação de API'
        verbose_name_plural = u'Paginações de APIs'