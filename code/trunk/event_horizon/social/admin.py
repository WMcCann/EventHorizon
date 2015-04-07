#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from social.models import *


class FacebookUserAdmin(admin.ModelAdmin):
    pass

class AdvertiserFacebookPageAdmin(admin.ModelAdmin):
    pass

class BrandFacebookPageAdmin(admin.ModelAdmin):
    pass

class CampaignFacebookPageAdmin(admin.ModelAdmin):
    pass

class InsightsFacebookPageAdmin(admin.ModelAdmin):
    pass

class AdvertiserTwitterProfileAdmin(admin.ModelAdmin):
    pass

class BrandTwitterProfileAdmin(admin.ModelAdmin):
    pass

class CampaignTwitterProfileAdmin(admin.ModelAdmin):
    pass

class AdvertiserYoutubeChannelAdmin(admin.ModelAdmin):
    pass

class BrandYoutubeChannelAdmin(admin.ModelAdmin):
    pass

class CampaignYoutubeChannelAdmin(admin.ModelAdmin):
    pass

class AnalyticsYoutubeChannelAdmin(admin.ModelAdmin):
    fields = ('youtube_channel', 'first_load', 'deleted')

    class Media:
        js = (
            '/public/lib/js/jquery-1.10.2.min.js',
            '/public/js/admin.js',
            )


admin.site.register(FacebookUser, FacebookUserAdmin)
admin.site.register(AdvertiserFacebookPage, AdvertiserFacebookPageAdmin)
admin.site.register(BrandFacebookPage, BrandFacebookPageAdmin)
admin.site.register(CampaignFacebookPage, CampaignFacebookPageAdmin)
admin.site.register(InsightsFacebookPage, InsightsFacebookPageAdmin)

admin.site.register(AdvertiserTwitterProfile, AdvertiserTwitterProfileAdmin)
admin.site.register(BrandTwitterProfile, BrandTwitterProfileAdmin)
admin.site.register(CampaignTwitterProfile, CampaignTwitterProfileAdmin)

admin.site.register(AdvertiserYoutubeChannel, AdvertiserYoutubeChannelAdmin)
admin.site.register(BrandYoutubeChannel, BrandYoutubeChannelAdmin)
admin.site.register(CampaignYoutubeChannel, CampaignYoutubeChannelAdmin)

admin.site.register(AnalyticsYoutubeChannel, AnalyticsYoutubeChannelAdmin)