#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from metrics_social.models import *


class FacebookMessageAdmin(admin.ModelAdmin):
    pass

class FacebookCommentAdmin(admin.ModelAdmin):
    pass

class FacebookLikeAdmin(admin.ModelAdmin):
    pass

class InsightsMetricAdmin(admin.ModelAdmin):
    pass

class EvolutionFacebookPageLikeAdmin(admin.ModelAdmin):
    pass

class TwitterMessageAdmin(admin.ModelAdmin):
    pass

class TwitterRetweetAdmin(admin.ModelAdmin):
    pass

class EvolutionTwitterProfileAdmin(admin.ModelAdmin):
    pass

class YoutubeVideoAdmin(admin.ModelAdmin):
    pass

class YoutubeCommentAdmin(admin.ModelAdmin):
    pass

class EvolutionYoutubeChannelAdmin(admin.ModelAdmin):
    pass

class FacebookInsightsReloadAdmin(admin.ModelAdmin):
    pass

admin.site.register(FacebookMessage, FacebookMessageAdmin)
admin.site.register(FacebookComment, FacebookCommentAdmin)
admin.site.register(FacebookLike, FacebookLikeAdmin)
admin.site.register(InsightsMetric, InsightsMetricAdmin)
admin.site.register(EvolutionFacebookPageLike, EvolutionFacebookPageLikeAdmin)
admin.site.register(TwitterMessage, TwitterMessageAdmin)
admin.site.register(TwitterRetweet, TwitterRetweetAdmin)
admin.site.register(EvolutionTwitterProfile, EvolutionTwitterProfileAdmin)
admin.site.register(YoutubeVideo, YoutubeVideoAdmin)
admin.site.register(YoutubeComment, YoutubeCommentAdmin)
admin.site.register(EvolutionYoutubeChannel, EvolutionYoutubeChannelAdmin)
admin.site.register(FacebookInsightsReload, FacebookInsightsReloadAdmin)