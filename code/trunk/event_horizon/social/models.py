#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime
from django.db import models

from third_party.facebook.exceptions import FacebookGenericError

from core.models import Brand, Person, Advertiser, Campaign
from services_social.models import FacebookConnection

from oauth2client.django_orm import CredentialsField

from south.modelsinspector import add_introspection_rules


class FacebookUser(models.Model):

    """
    FacebookUser
    =========

    FacebookUser is a model to store all public info about facebook user.

    e.g. 
    FacebookUser: 
    100000845187724
    Johann Vivot

    """

    person = models.OneToOneField(Person, verbose_name=u'Pessoa', blank=False)
    facebook_id = models.CharField(verbose_name=u'ID Facebook', max_length=255, blank=False, unique=True)
    name = models.CharField(verbose_name=u'Nome', max_length=255, blank=True, null=True)
    first_name = models.CharField(verbose_name=u'Primeiro nome', max_length=255, blank=True, null=True)
    middle_name = models.CharField(verbose_name=u'Nome do meio', max_length=255, blank=True, null=True)
    last_name = models.CharField(verbose_name=u'Último nome', max_length=255, blank=True, null=True)
    link = models.URLField(verbose_name=u'Link', max_length=255, blank=False)
    username = models.CharField(verbose_name=u'Usuário', max_length=255, blank=True, null=True)
    gender = models.CharField(verbose_name=u'Sexo', max_length=255, blank=True, null=True)
    locale = models.CharField(verbose_name=u'Localidade', max_length=255, blank=True, null=True)
    picture = models.URLField(verbose_name=u'Foto', max_length=255, blank=True, null=True)
    page = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Usuário do Facebook'
        verbose_name_plural = u'Usuários do Facebook'


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.first_name = self.first_name.upper()
        self.middle_name = self.middle_name.upper()
        self.last_name = self.last_name.upper()
        self.gender = self.gender.upper()
        super(FacebookUser, self).save(*args, **kwargs)

    @classmethod
    def get_facebook_user(cls, client, facebook_id):
        
        """
        method to retrieve facebook user, if it doesn't exist it'll be created

        """

        try:
            fbu = cls.objects.get(facebook_id__exact=facebook_id, deleted=False)
        except cls.DoesNotExist:
            try:
                user_data = client.obj_id(
                    facebook_id,
                    fields='id,name,first_name,middle_name,last_name,link,username,gender,locale,picture',
                    )
            except FacebookGenericError:
                user_data = client.obj_id(
                    facebook_id,
                    fields='id,name,link,picture',
                    )

                person = Person(
                    name=user_data[u'name'] if u'name' in user_data else None,
                    )
                person.save()

                fbu = cls(
                    person=person,
                    facebook_id=user_data[u'id'],
                    name=user_data[u'name'] if u'name' in user_data else None,
                    link=user_data[u'link'] if u'link' in user_data else None,
                    page=True,
                    )

                if u'picture' in user_data:
                    fbu.picture = user_data[u'picture'][u'data'][u'url']
            else:
                person = Person(
                    name=user_data[u'name'] if u'name' in user_data else None,
                    gender=user_data[u'gender'] if u'gender' in user_data else None,
                    )
                person.save()

                fbu = cls(
                    person=person,
                    facebook_id=user_data[u'id'],
                    name=user_data[u'name'] if u'name' in user_data else None,
                    first_name=user_data[u'first_name'] if u'first_name' in user_data else None,
                    middle_name=user_data[u'middle_name'] if u'middle_name' in user_data else None,
                    last_name=user_data[u'last_name'] if u'last_name' in user_data else None,
                    link=user_data[u'link'] if u'link' in user_data else None,
                    username=user_data[u'username'] if u'username' in user_data else None,
                    gender=user_data[u'gender'] if u'gender' in user_data else None,
                    locale=user_data[u'locale'] if u'locale' in user_data else None,
                    picture=user_data[u'picture'][u'data'][u'url'] if u'picture' in user_data else None,
                    page=False,
                    )

            fbu.save()
        return fbu


class FacebookPage(models.Model):
    """
    FacebookPage
    =========

    FacebookPage is a parent model to store main info about facebook page.

    e.g. 
    FacebookPage: 
    117750778311686
    Chevrolet Brasil

    """

    name = models.CharField(verbose_name=u'Nome', max_length=255, blank=False)
    facebook_id = models.CharField(verbose_name=u'ID Facebook', max_length=255, blank=False, unique=True)
    link = models.URLField(verbose_name=u'Link', max_length=255, blank=True, null=True)
    talking_about = models.IntegerField(verbose_name=u'Talking about', default=0, blank=False)
    likes = models.IntegerField(verbose_name=u'Likes', default=0, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Página do Facebook'
        verbose_name_plural = u'Páginas do Facebook'


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(FacebookPage, self).save(*args, **kwargs)


class AdvertiserFacebookPage(FacebookPage):

    """
    AdvertiserFacebookPage
    =========

    AdvertiserFacebookPage is a model to store main info about advertiser facebook page.

    e.g. 
    AdvertiserFacebookPage: 
    117750778311686
    Chevrolet Brasil

    """

    advertiser = models.ForeignKey(Advertiser, verbose_name=u'Advertiser')
    first_load = models.BooleanField(verbose_name=u'Primeiro load', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Página do Facebook do Advertiser'
        verbose_name_plural = u'Páginas do Facebook dos Advertisers'


class BrandFacebookPage(FacebookPage):

    """
    BrandFacebookPage
    =========

    BrandFacebookPage is a model to store main info about brand facebook page.

    e.g. 
    BrandFacebookPage: 
    117750778311686
    Chevrolet Brasil

    """

    brand = models.ForeignKey(Brand, verbose_name=u'Marca')
    first_load = models.BooleanField(verbose_name=u'Primeiro load', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Página do Facebook da Marca'
        verbose_name_plural = u'Páginas do Facebook das Marcas'


class CampaignFacebookPage(FacebookPage):

    """
    CampaignFacebookPage
    =========

    CampaignFacebookPage is a model to store main info about campaign facebook page.

    e.g. 
    CampaignFacebookPage: 
    117750778311686
    Chevrolet Brasil

    """

    campaign = models.ForeignKey(Campaign, verbose_name=u'Campaign')
    first_load = models.BooleanField(verbose_name=u'Primeiro load', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Página do Facebook do Campanha'
        verbose_name_plural = u'Páginas do Facebook das Campanhas'


class InsightsFacebookPage(models.Model):

    """
    InsightsFacebookPage
    =========

    InsightsFacebookPage is a model to store main info about facebook page insights.

    e.g. 
    InsightsFacebookPage: 
    117750778311686
    Chevrolet Brasil

    """

    facebook_page = models.ForeignKey(FacebookPage, verbose_name=u'Página do Facebook', blank=False)
    first_load_daily = models.BooleanField(verbose_name=u'Primeiro Load Daily', default=False, blank=False)
    first_load_weekly = models.BooleanField(verbose_name=u'Primeiro Load Weekly', default=False, blank=False)
    first_load_days_28 = models.BooleanField(verbose_name=u'Primeiro Load Days 28', default=False, blank=False)
    first_load_dimensions = models.BooleanField(verbose_name=u'Primeiro Load Dimensões', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.facebook_page.name

    class Meta:
        ordering = [u'facebook_page']
        verbose_name = u'Insights da Página do Facebook'
        verbose_name_plural = u'Insights das Páginas do Facebook'


class TwitterProfile(models.Model):
    """
    TwitterProfile
    =========

    TwitterProfile is a parent model to store main info about twitter profile.

    e.g. 
    TwitterProfile: 
    140582641
    chevroletbrasil

    """

    name = models.CharField(verbose_name=u'Nome', max_length=255, blank=False)
    screen_name = models.CharField(verbose_name=u'Usuário', max_length=255, blank=False)
    twitter_id = models.CharField(verbose_name=u'ID Twitter', max_length=255, blank=False, unique=True)
    followers_count = models.IntegerField(verbose_name=u'Followers', default=0, blank=False)
    friends_count = models.IntegerField(verbose_name=u'Following', default=0, blank=False)
    listed_count = models.IntegerField(verbose_name=u'Listado', default=0, blank=False)
    favourites_count = models.IntegerField(verbose_name=u'Favoritado', default=0, blank=False)
    statuses_count = models.IntegerField(verbose_name=u'Tweets', default=0, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Perfil do Twitter'
        verbose_name_plural = u'Perfis do Twitter'


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(TwitterProfile, self).save(*args, **kwargs)


class AdvertiserTwitterProfile(TwitterProfile):

    """
    AdvertiserTwitterProfile
    =========

    AdvertiserTwitterProfile is a model to store main info about advertiser twitter profile.

    e.g. 
    AdvertiserTwitterProfile: 
    140582641
    chevroletbrasil

    """

    advertiser = models.ForeignKey(Advertiser, verbose_name=u'Advertiser')
    first_load = models.BooleanField(verbose_name=u'Primeiro load', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Perfil do Twitter do Advertiser'
        verbose_name_plural = u'Perfis do Twitter dos Advertisers'


class BrandTwitterProfile(TwitterProfile):

    """
    BrandTwitterProfile
    =========

    BrandTwitterProfile is a model to store main info about brand twitter profile.

    e.g. 
    BrandTwitterProfile: 
    140582641
    chevroletbrasil

    """

    brand = models.ForeignKey(Brand, verbose_name=u'Marca')
    first_load = models.BooleanField(verbose_name=u'Primeiro load', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Perfil do Twitter da Marca'
        verbose_name_plural = u'Perfis do Twitter das Marcas'


class CampaignTwitterProfile(TwitterProfile):

    """
    CampaignTwitterProfile
    =========

    CampaingTwitterProfile is a model to store main info about campaign twitter profile.

    e.g. 
    CampaignTwitterProfile: 
    140582641
    chevroletbrasil

    """

    campaign = models.ForeignKey(Campaign, verbose_name=u'Campanha')
    first_load = models.BooleanField(verbose_name=u'Primeiro load', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'name']
        verbose_name = u'Perfil do Twitter da Campanha'
        verbose_name_plural = u'Perfis do Twitter das Campanhas'


class YoutubeChannel(models.Model):
    """
    YoutubeChannel
    =========

    YoutubeChannel is a parent model to store main info about youtube channel.

    e.g. 
    YoutubeChannel: 
    UCPN_tMDcDoQCxoP4fVkQAxw
    Vivo

    """

    username = models.CharField(verbose_name=u'Usuário', max_length=255, blank=False)
    youtube_id = models.CharField(verbose_name=u'ID Youtube', max_length=255, blank=False, unique=True)
    views_count = models.IntegerField(verbose_name=u'Views', default=0, blank=False)
    videos_count = models.IntegerField(verbose_name=u'Videos', default=0, blank=False)
    subscribers_count = models.IntegerField(verbose_name=u'Listado', default=0, blank=False)


    def __unicode__(self):
        return self.username

    class Meta:
        ordering = [u'username']
        verbose_name = u'Canal do Youtube'
        verbose_name_plural = u'Canais do Youtube'


    def save(self, *args, **kwargs):
        super(YoutubeChannel, self).save(*args, **kwargs)


class AdvertiserYoutubeChannel(YoutubeChannel):

    """
    AdvertiserYoutubeChannel
    =========

    AdvertiserYoutubeChannel is a model to store main info about advertiser youtube channel.

    e.g. 
    AdvertiserYoutubeChannel: 
    UCPN_tMDcDoQCxoP4fVkQAxw
    Vivo

    """

    advertiser = models.ForeignKey(Advertiser, verbose_name=u'Advertiser')
    first_load = models.BooleanField(verbose_name=u'Primeiro load', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.username

    class Meta:
        ordering = [u'username']
        verbose_name = u'Canal do Youtube do Advertiser'
        verbose_name_plural = u'Canais do Youtube dos Advertisers'


class BrandYoutubeChannel(YoutubeChannel):

    """
    BrandYoutubeChannel
    =========

    BrandYoutubeChannel is a model to store main info about brand youtube channel.

    e.g. 
    BrandYoutubeChannel: 
    UCPN_tMDcDoQCxoP4fVkQAxw
    Vivo

    """

    brand = models.ForeignKey(Brand, verbose_name=u'Marca')
    first_load = models.BooleanField(verbose_name=u'Primeiro load', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.username

    class Meta:
        ordering = [u'username']
        verbose_name = u'Canal do Youtube da Marca'
        verbose_name_plural = u'Canais do Youtube das Marcas'


class CampaignYoutubeChannel(YoutubeChannel):

    """
    CampaignYoutubeChannel
    =========

    CampaingYoutubeChannel is a model to store main info about campaign youtube channel.

    e.g. 
    CampaignYoutubeChannel: 
    UCPN_tMDcDoQCxoP4fVkQAxw
    Vivo

    """

    campaign = models.ForeignKey(Campaign, verbose_name=u'Campanha')
    first_load = models.BooleanField(verbose_name=u'Primeiro load', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.username

    class Meta:
        ordering = [u'username']
        verbose_name = u'Canal do Youtube da Campanha'
        verbose_name_plural = u'Canais do Youtube das Campanhas'


# instrospection rules for south
add_introspection_rules([], ["^oauth2client\.django_orm\.CredentialsField"])
class AnalyticsYoutubeChannel(models.Model):

    """
    AnalyticsYoutubeChannel
    =========

    AnalyticsYoutubeChannel is a model to store main info about analytics from a youtube channel.

    e.g. 
    AnalyticsYoutubeChannel: 
    UCRojKYdkvZcRQX1Vu7wEU5g
    chevroletbrasil

    """

    email = models.EmailField(verbose_name=u'E-mail', blank=False, primary_key=True)
    credential = CredentialsField()
    youtube_channel = models.ForeignKey(YoutubeChannel, verbose_name=u'Canal do Youtube', blank=True, null=True)
    first_load = models.BooleanField(verbose_name=u'Primeiro Load', default=False, blank=False)


    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.email

    class Meta:
        ordering = [u'youtube_channel']
        verbose_name = u'Analytics de Canal do Youtube'
        verbose_name_plural = u'Analytics de Canais do Youtube'