#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime
from django.db import models

from core.models import Person, APIError
from social.models import FacebookUser, FacebookPage, InsightsFacebookPage, TwitterProfile, YoutubeChannel


class FacebookMessage(models.Model):

    """
    FacebookMessage
    =========

    FacebookMessage is a model to store all facebook massage sent to/from a page.

    e.g. 
    FacebookMessage: 
    117750778311686_504062606347166

    """

    facebook_page = models.ForeignKey(FacebookPage, verbose_name=u'Página do Facebook', blank=False)
    facebook_id = models.CharField(verbose_name=u'ID Facebook', max_length=255, blank=False)
    author_facebook_id = models.CharField(verbose_name=u'ID Facebook do Autor', max_length=255, blank=False)
    author = models.ForeignKey(FacebookUser, verbose_name=u'Autor', blank=True, null=True)
    message = models.TextField(verbose_name=u'Mensagem', blank=False)
    created_time = models.DateTimeField(verbose_name=u'Criado em', blank=False)
    message_type = models.CharField(verbose_name=u'Tipo', max_length=255, blank=False)
    likes = models.BigIntegerField(verbose_name=u'Likes', default=0, blank=False)
    comments = models.BigIntegerField(verbose_name=u'Comentários', default=0, blank=False)
    shares = models.BigIntegerField(verbose_name=u'Compartilhamentos', default=0, blank=False)

    loaded_comments = models.BooleanField(verbose_name=u'Baixado todos comentários', default=False, blank=False)
    loaded_likes = models.BooleanField(verbose_name=u'Baixado todos likes', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.facebook_id

    class Meta:
        unique_together = ('facebook_page', 'facebook_id',)
        ordering = [u'-created_time']
        verbose_name = u'Mensagem do Facebook'
        verbose_name_plural = u'Mensagens do Facebook'

    @classmethod
    def row_save(cls, row, **kwargs):
        # saving message
        try:
            fbm = cls.objects.get(
                facebook_page=kwargs.get('fp'),
                facebook_id__exact=row[u'id'],
                deleted=False,
                )
        except cls.DoesNotExist:
            try:
                if u'likes' in row and u'count' in row[u'likes']:
                    likes = row[u'likes'][u'count']
                else:
                    likes = 0

                if u'comments' in row and u'count' in row[u'comments']:
                    comments = row[u'comments'][u'count']
                else:
                    comments = 0

                content = u''
                if u'message' in row:
                    content = u'%s' % row[u'message']

                if u'story' in row:
                    content = u'%s %s' % (content, row[u'story'])

                if u'picture' in row:
                    content = u'%s %s' % (content, row[u'picture'])

                if u'link' in row:
                    content = u'%s %s' % (content, row[u'link'])

                fbm = cls(
                    facebook_page=kwargs.get('fp'),
                    facebook_id=row[u'id'],
                    author_facebook_id=row[u'from'][u'id'],
                    message=content,
                    created_time=datetime.strptime(row[u'created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
                    message_type=row[u'type'],
                    likes=likes,
                    comments=comments,
                    shares=row[u'shares'][u'count'] if u'shares' in row else 0,
                    )
            except Exception, e:
                err = APIError(
                    app_name=u'metrics_social',
                    model_name='FacebookMessage',
                    error=u'%s: %s' % (Exception, str(e)),
                    response=row,
                    )
                err.save()
                return u'Inserted error message: %s %s' % (Exception, str(e))
            else:
                fbm.save()
                return u'Inserted message %s' % fbm.facebook_id
        else:
            return u'Message already exists: %s' % fbm.facebook_id


class FacebookComment(models.Model):

    """
    FacebookComment
    =========

    FacebookComment is a model to store all facebook comment made about a message to/from a page.

    e.g. 
    FacebookComment: 
    503920666361360_1566834

    """

    facebook_id = models.CharField(verbose_name=u'ID Facebook', max_length=255, blank=False)
    message = models.ForeignKey(FacebookMessage, verbose_name=u'Mensagem')
    author_facebook_id = models.CharField(verbose_name=u'ID Facebook do Autor', max_length=255, blank=False)
    author = models.ForeignKey(FacebookUser, verbose_name=u'Autor', blank=True, null=True)
    comment = models.TextField(verbose_name=u'Comentário', blank=False)
    created_time = models.DateTimeField(verbose_name=u'Criado em', blank=False)
    likes = models.BigIntegerField(verbose_name=u'Likes', default=0, blank=False)
    user_likes = models.BooleanField(verbose_name=u'Author Curte')

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.facebook_id

    class Meta:
        unique_together = ('facebook_id', 'message',)
        ordering = [u'-created_time']
        verbose_name = u'Comentário da Mensagem do Facebook'
        verbose_name_plural = u'Comentários das Mensagens do Facebook'

    @classmethod
    def row_save(cls, row, **kwargs):
        # saving message
        try:
            fbc = cls.objects.get(
                message=kwargs.get('fbmowner'),
                facebook_id__exact=row[u'id'],
                deleted=False
                )
        except cls.DoesNotExist:
            try:
                fbc = cls(
                    facebook_id=row[u'id'],
                    message=kwargs.get('fbmowner'),
                    author_facebook_id=row[u'from'][u'id'],
                    comment=row[u'message'],
                    created_time=datetime.strptime(row[u'created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
                    likes=row[u'like_count'],
                    user_likes=row[u'user_likes'],
                    )
            except Exception, e:
                err = APIError(
                    app_name=u'metrics_social',
                    model_name='FacebookComment',
                    error=u'%s: %s' % (Exception, e),
                    response=row,
                    )
                err.save()
                return u'Inserted error comment: %s %s' % (Exception, str(e))
            else:
                fbc.save()
                return u'Inserted comment %s' % fbc.facebook_id
        else:
            return u'Comment already exists: %s' % fbc.facebook_id


class FacebookLike(models.Model):

    """
    FacebookLike
    =========

    FacebookLike is a model to store all facebook like in a message to/from a page.

    """

    message = models.ForeignKey(FacebookMessage, verbose_name=u'Mensagem')
    author_facebook_id = models.CharField(verbose_name=u'ID Facebook do Autor', max_length=255, blank=False)
    author = models.ForeignKey(FacebookUser, verbose_name=u'Autor', blank=True, null=True)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.author_facebook_id

    class Meta:
        unique_together = ('message', 'author_facebook_id',)
        ordering = [u'-created_at']
        verbose_name = u'Like da Mensagem do Facebook'
        verbose_name_plural = u'Likes das Mensagens do Facebook'

    @classmethod
    def row_save(cls, row, **kwargs):
        # saving message
        try:
            fbl = cls.objects.get(
                message=kwargs.get('fbmowner'),
                author_facebook_id__exact=row[u'id'],
                deleted=False,
                )
        except cls.DoesNotExist:
            try:
                fbl = cls(
                    message=kwargs.get('fbmowner'),
                    author_facebook_id=row[u'id'],
                    )
            except Exception, e:
                err = APIError(
                    app_name=u'metrics_social',
                    model_name='FacebookLike',
                    error=u'%s: %s' % (Exception, e),
                    response=row,
                    )
                err.save()
                return u'Inserted error like: %s %s' % (Exception, str(e))
            else:
                fbl.save()
                return u'Inserted like of %s in %s' % (fbl.author_facebook_id, fbl.message.facebook_id)
        else:
            return u'Like of author %s already exists in %s' % (fbl.author_facebook_id, fbl.message.facebook_id)



class InsightsMetric(models.Model):

    """
    InsightsMetric
    =========

    InsightsMetric is a model to store all facebook insights metrics.

    """

    facebook_page = models.ForeignKey(InsightsFacebookPage, verbose_name=u'Página do Facebook', blank=False)
    facebook_message = models.ForeignKey(FacebookMessage, verbose_name=u'Mensagem do Facebook', blank=True, null=True)
    day = models.DateField(verbose_name=u'Data', blank=True, null=True)
    title = models.CharField(verbose_name=u'Título', max_length=255, blank=False)
    description = models.TextField(verbose_name=u'Descrição', blank=False)
    metric = models.CharField(verbose_name=u'Métrica', max_length=255, blank=False)
    dimension = models.CharField(verbose_name=u'Dimensão', max_length=255, blank=True, null=True)
    value = models.BigIntegerField(verbose_name=u'Valor', default=0, blank=False)
    period = models.CharField(verbose_name=u'Período', max_length=255, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = [u'-created_at']
        verbose_name = u'Métrica do Facebook Insights da Página'
        verbose_name_plural = u'Métricas do Facebook Insights das Páginas'



class EvolutionFacebookPageLike(models.Model):

    """
    EvolutionFacebookPageLike
    =========

    EvolutionFacebookPageLike is a model to store the evolution of fans growth of a facebook page.

    e.g. 
    EvolutionFacebookPageLike: 
    Chevrolet Brasil

    """

    facebook_page = models.ForeignKey(FacebookPage, verbose_name=u'Página do Facebook', blank=False)
    likes = models.BigIntegerField(verbose_name=u'Likes', default=0, blank=False)
    date = models.DateTimeField(verbose_name=u'Data do Registro', default=datetime.now, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.facebook_page.name

    class Meta:
        ordering = [u'facebook_page']
        verbose_name = u'Evolução de Likes na Facebook Page'
        verbose_name_plural = u'Evoluções de Likes nas Facebook Pages'


class TwitterMessage(models.Model):

    """
    TwitterMessage
    =========

    TwitterMessage is a model to store all twitter massage sent to/from a profile.

    e.g. 
    TwitterMessage: 
    383280194846724100

    """

    twitter_profile = models.ForeignKey(TwitterProfile, verbose_name=u'Pefil do Twitter', blank=False)
    twitter_id = models.CharField(verbose_name=u'ID Twitter', max_length=255, blank=False)
    author_twitter_id = models.CharField(verbose_name=u'ID Twitter do Autor', max_length=255, blank=False)
    #author = models.ForeignKey(TwitterUser, verbose_name=u'Autor', blank=True, null=True)
    message = models.TextField(verbose_name=u'Mensagem', blank=False)
    created_time = models.DateTimeField(verbose_name=u'Criado em', blank=False)
    favorites = models.BigIntegerField(verbose_name=u'Favoritos', default=0, blank=False)
    retweets = models.BigIntegerField(verbose_name=u'Retweets', default=0, blank=False)

    loaded_retweets = models.BooleanField(verbose_name=u'Baixado todos retweets', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.twitter_id

    class Meta:
        unique_together = ('twitter_profile', 'twitter_id',)
        ordering = [u'-created_time']
        verbose_name = u'Mensagem do Twitter'
        verbose_name_plural = u'Mensagens do Twitter'


class TwitterRetweet(models.Model):

    """
    TwitterRetweet
    =========

    TwitterRetweet is a model to store all retweet of a tweet from a twitter profile.

    """

    message = models.ForeignKey(TwitterMessage, verbose_name=u'Mensagem')
    author_twitter_id = models.CharField(verbose_name=u'ID Twitter do Autor', max_length=255, blank=False)
    #author = models.ForeignKey(FacebookUser, verbose_name=u'Autor', blank=True, null=True)
    created_time = models.DateTimeField(verbose_name=u'Criado em', blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.author_twitter_id

    class Meta:
        unique_together = ('message', 'author_twitter_id',)
        ordering = [u'-created_at']
        verbose_name = u'Retweet da Mensagem do Twitter'
        verbose_name_plural = u'Retweet das Mensagens do Twitter'


class EvolutionTwitterProfile(models.Model):

    """
    EvolutionTwitterProfile
    =========

    EvolutionTwitterProfile is a model to store the evolution of fans growth of a twitter profile.

    e.g. 
    EvolutionTwitterProfile: 
    Chevrolet Brasil

    """

    twitter_profile = models.ForeignKey(TwitterProfile, verbose_name=u'Pefil do Twitter', blank=False)
    followers_count = models.BigIntegerField(verbose_name=u'Followers', default=0, blank=False)
    friends_count = models.BigIntegerField(verbose_name=u'Following', default=0, blank=False)
    listed_count = models.BigIntegerField(verbose_name=u'Listado', default=0, blank=False)
    favourites_count = models.BigIntegerField(verbose_name=u'Favoritado', default=0, blank=False)
    statuses_count = models.BigIntegerField(verbose_name=u'Tweets', default=0, blank=False)
    date = models.DateTimeField(verbose_name=u'Data do Registro', default=datetime.now, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.twitter_profile.name

    class Meta:
        ordering = [u'twitter_profile']
        verbose_name = u'Evolução de Fans no Perfil do Twitter'
        verbose_name_plural = u'Evoluções de Fans nos Perfis do Twitter'


class YoutubeVideo(models.Model):

    """
    YoutubeVideo
    =========

    YoutubeVideo is a model to store all youtube videos from some channel.

    e.g. 
    YoutubeVideo: 
    Tvz_SWMOZHA

    """

    youtube_channel = models.ForeignKey(YoutubeChannel, verbose_name=u'Canal do Youtube', blank=False)
    youtube_id = models.CharField(verbose_name=u'ID Youtube', max_length=255, blank=False)
    title = models.CharField(verbose_name=u'Título', max_length=255, blank=False)
    description = models.TextField(verbose_name=u'Descrição', blank=False)
    created_time = models.DateTimeField(verbose_name=u'Criado em', blank=False)
    views = models.BigIntegerField(verbose_name=u'Vizualizações', default=0, blank=False)
    likes = models.BigIntegerField(verbose_name=u'Likes', default=0, blank=False)
    dislikes = models.BigIntegerField(verbose_name=u'Dislikes', default=0, blank=False)
    favorites = models.BigIntegerField(verbose_name=u'Favoritos', default=0, blank=False)
    comments = models.BigIntegerField(verbose_name=u'Comentários', default=0, blank=False)

    loaded_comments = models.BooleanField(verbose_name=u'Baixado todos comentários', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.youtube_id

    class Meta:
        unique_together = ('youtube_channel', 'youtube_id',)
        ordering = [u'-created_time']
        verbose_name = u'Video do Youtube'
        verbose_name_plural = u'Videos do Youtube'

    @classmethod
    def row_save(cls, row, **kwargs):
        # saving video
        if row[u'kind'] == u'youtube#video':
            try:
                ytv = cls.objects.get(
                    youtube_channel=kwargs.get('yc'),
                    youtube_id__exact=row[u'id'],
                    deleted=False,
                    )
            except cls.DoesNotExist:
                try:
                    ytv = cls(
                        youtube_channel=kwargs.get('yc'),
                        youtube_id=row[u'id'],
                        title=row[u'snippet'][u'title'],
                        description=row[u'snippet'][u'description'],
                        created_time=datetime.strptime(row[u'snippet'][u'publishedAt'], '%Y-%m-%dT%H:%M:%S.000Z'),
                        views=row[u'statistics'][u'viewCount'],
                        likes=row[u'statistics'][u'likeCount'],
                        dislikes=row[u'statistics'][u'dislikeCount'],
                        favorites=row[u'statistics'][u'favoriteCount'],
                        comments=row[u'statistics'][u'commentCount'],
                        )
                except Exception, e:
                    err = APIError(
                        app_name=u'metrics_social',
                        model_name='YoutubeVideo',
                        error=u'%s: %s' % (Exception, str(e)),
                        response=row,
                        )
                    err.save()
                    return u'Inserted error video: %s %s' % (Exception, str(e))
                else:
                    ytv.save()
                    return u'Inserted video %s' % ytv.youtube_id
            else:
                return u'Video already exists: %s' % ytv.youtube_id



class YoutubeComment(models.Model):

    """
    YoutubeComment
    =========

    YoutubeComment is a model to store all youtube comment made about a video.

    e.g. 
    YoutubeComment: 
    OHoJmxjJi1vq7oftZSOL6v8sCykFJWLYZqDco5MMCC0

    """

    youtube_id = models.CharField(verbose_name=u'ID Youtube', max_length=255, blank=False)
    video = models.ForeignKey(YoutubeVideo, verbose_name=u'Video')
    author_youtube_username = models.CharField(verbose_name=u'Username do Youtube do Autor', max_length=255, blank=False)
    #author = models.ForeignKey(FacebookUser, verbose_name=u'Autor', blank=True, null=True)
    title = models.TextField(verbose_name=u'Título', blank=False)
    comment = models.TextField(verbose_name=u'Comentário', blank=False)
    created_time = models.DateTimeField(verbose_name=u'Criado em', blank=False)


    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.youtube_id

    class Meta:
        unique_together = ('youtube_id', 'video',)
        ordering = [u'-created_time']
        verbose_name = u'Comentário do Vídeo do Youtube'
        verbose_name_plural = u'Comentários dos Vídeos do Youtube'


class EvolutionYoutubeChannel(models.Model):

    """
    EvolutionYoutubeChannel
    =========

    EvolutionYoutubeChannel is a model to store the evolution of fans growth of a youtube channel.

    e.g. 
    EvolutionYoutubeChannel: 
    Vivo

    """

    youtube_channel = models.ForeignKey(YoutubeChannel, verbose_name=u'Pefil do Twitter', blank=False)
    views_count = models.IntegerField(verbose_name=u'Views', default=0, blank=False)
    videos_count = models.IntegerField(verbose_name=u'Videos', default=0, blank=False)
    subscribers_count = models.IntegerField(verbose_name=u'Listado', default=0, blank=False)
    date = models.DateTimeField(verbose_name=u'Data do Registro', default=datetime.now, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.youtube_channel.username

    class Meta:
        ordering = [u'youtube_channel']
        verbose_name = u'Evolução do Canal do Youtube'
        verbose_name_plural = u'Evoluções de Canais do Youtube'


class FacebookMessageReload(models.Model):

    """
    FacebookMessageReload
    =========

    FacebookMessageReload is a model to store facebook message to reload.

    e.g. 
    FacebookMessageReload: 
    117750778311686_228414790643669
    curti? por favor? www.facebook.com/pages/Cristiano-Ronaldo-o-melhor/154309704762961

    """

    message = models.ForeignKey(FacebookMessage, verbose_name=u'Message')
    comments = models.BooleanField(verbose_name=u'Reload Comments', default=False, blank=False)
    likes = models.BooleanField(verbose_name=u'Reload Likes', default=False, blank=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.message.facebook_id

    class Meta:
        ordering = [u'-created_at']
        verbose_name = u'Reload Post do Facebook'
        verbose_name_plural = u'Reload Posts do Facebook'


class FacebookInsightsReload(models.Model):

    """
    FacebookInsightsReload
    =========

    FacebookInsightsReload is a model to store facebook insights to reload.

    e.g. 
    FacebookInsightsReload: 
    117750778311686_228414790643669
    curti? por favor? www.facebook.com/pages/Cristiano-Ronaldo-o-melhor/154309704762961

    """

    facebook_page = models.ForeignKey(FacebookPage, verbose_name=u'Página do Facebook', blank=False)
    reload_post_level = models.BooleanField(verbose_name=u'Post Level', default=False, blank=False)
    reload_post_level_dimensions = models.BooleanField(verbose_name=u'Post Level Dimensões', default=False, blank=False)
    reload_daily = models.BooleanField(verbose_name=u'Reload Daily', default=False, blank=False)
    reload_weekly = models.BooleanField(verbose_name=u'Reload Weekly', default=False, blank=False)
    reload_days_28 = models.BooleanField(verbose_name=u'Reload Days 28', default=False, blank=False)
    reload_dimensions = models.BooleanField(verbose_name=u'Reload Dimensões', default=False, blank=False)

    since = models.DateTimeField(verbose_name=u'De', default=datetime.now, blank=False, null=False)
    until = models.DateTimeField(verbose_name=u'Até', default=datetime.now, blank=False, null=False)

    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', default=datetime.now, blank=True, auto_now=True, auto_now_add=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', default=datetime.now, blank=True)
    deleted = models.BooleanField(verbose_name=u'Deletado', default=False, blank=False)


    def __unicode__(self):
        return self.facebook_page.name

    class Meta:
        ordering = [u'-created_at']
        verbose_name = u'Reload Insights do Facebook'
        verbose_name_plural = u'Reloads Insights do Facebook'