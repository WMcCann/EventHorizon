#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import httplib2
import tweepy
import json
import datetime

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.db import connection
from django.db.models import Max

from dateutil.relativedelta import relativedelta

from core.models import Brand, Company
from metrics_social.models import EvolutionFacebookPageLike, \
    EvolutionTwitterProfile, EvolutionYoutubeChannel, FacebookMessage, TwitterMessage, YoutubeVideo

from dashboard.utils import human_format


def select_brand(request):

    """
    View to dashboard.

    URI: /dashboard

    """

    if request.method == 'POST':
        brand_id = request.POST.get('brand_id', None)
        if brand_id:
            return redirect('/dashboard/%s' % brand_id)

    wmccann = get_object_or_404(Company, id=1)
    brands = Brand.objects.filter(
        advertiser__company_owner=wmccann,
        deleted=False,
        )

    return render_to_response('select_brand.html',
                              {'brands': brands},
                              context_instance=RequestContext(request))


def dashboard(request, dash_id):

    """
    View to dashboard.

    URI: /dashboard

    """

    brand = get_object_or_404(Brand, id=dash_id)
    competitors = [b for b in Brand.objects.filter(
                                country=brand.country, 
                                category=brand.category) 
                                    if b != brand]

    # load files
    filename_fans = os.path.join(
        settings.PROJECT_ROOT_PATH, 'queries', 'total_fans.sql')
    filename_interactions = os.path.join(
        settings.PROJECT_ROOT_PATH, 'queries', 'interactions_by_month_and_socialnetwork.sql')
    filename_type = os.path.join(
        settings.PROJECT_ROOT_PATH, 'queries', 'total_by_interaction_type.sql')

    try:
        with open(filename_fans) as f:
            lines = f.readlines()
        query_fans = ''.join(lines)

        with open(filename_interactions) as f:
            lines = f.readlines()
        query_interactions = ''.join(lines)

        with open(filename_type) as f:
            lines = f.readlines()
        query_type = ''.join(lines)
    except IOError:
        raise Http404

    cursor = connection.cursor()

    end_date = datetime.date.today()
    start_date = end_date + relativedelta(months=-6)
    end_date = end_date + relativedelta(days=-1)

    cursor.execute(query_fans % (
        brand.id, 
        brand.name, 
        start_date.strftime('%Y%m%d'), 
        end_date.strftime('%Y%m%d'),
        ))

    data = {
        u'id': brand.id,
        u'name': brand.name, 
        u'fans': human_format(cursor.fetchone()[0]),
        u'interaction': {
            u'categories': [],
            u'series': []
            },
        u'type': {},
        }

    cursor.execute(query_interactions % (
        brand.id, 
        brand.name, 
        start_date.strftime('%Y%m%d'), 
        end_date.strftime('%Y%m%d'),
        ))

    for row in cursor.fetchall():
        data[u'interaction'][u'categories'].append(u'%s/%s' % (row[2], row[1]))
        data[u'interaction'][u'series'].append(row[6])

    cursor.execute(query_type % (
        brand.id, 
        brand.name, 
        start_date.strftime('%Y%m%d'), 
        end_date.strftime('%Y%m%d'),
        ))

    for row in cursor.fetchall():
        data[u'type'][row[1]] = row[2]

    brands = [data]

    for competitor in competitors:
        cursor.execute(query_fans % (
            competitor.id, 
            competitor.name, 
            start_date.strftime('%Y%m%d'), 
            end_date.strftime('%Y%m%d'),
            ))

        data = {
            u'id': competitor.id,
            u'name': competitor.name,
            u'fans': human_format(cursor.fetchone()[0]),
            u'interaction': {
                u'categories': [],
                u'series': []
                },
            u'type': {},
            }

        cursor.execute(query_interactions % (
            competitor.id, 
            competitor.name, 
            start_date.strftime('%Y%m%d'), 
            end_date.strftime('%Y%m%d'),
            ))

        for row in cursor.fetchall():
            data[u'interaction'][u'categories'].append(u'%s/%s' % (row[2], row[1]))
            data[u'interaction'][u'series'].append(row[6])

        cursor.execute(query_type % (
            competitor.id, 
            competitor.name, 
            start_date.strftime('%Y%m%d'), 
            end_date.strftime('%Y%m%d'),
            ))

        for row in cursor.fetchall():
            data[u'type'][row[1]] = row[2]

        brands.append(data)

    return render_to_response('dashboard.html',
                              {'dash_id': brand.id,
                               'brands': brands,},
                              context_instance=RequestContext(request))


def customer(request, dash_id, brand_id):

    """
    View to customer detail dashboard.

    URI: /dashboard/customer

    """

    brand = get_object_or_404(Brand, id=brand_id)
    
    # load file
    filename_fans = os.path.join(
        settings.PROJECT_ROOT_PATH, 'queries', 'total_fans_by_socialnetwork.sql')
    filename_interactions = os.path.join(
        settings.PROJECT_ROOT_PATH, 'queries', 'interactions_by_day_and_socialnetwork.sql')
    try:
        with open(filename_fans) as f:
            lines = f.readlines()
        query_fans = ''.join(lines)

        with open(filename_interactions) as f:
            lines = f.readlines()
        query_interactions = ''.join(lines)
    except IOError:
        raise Http404

    cursor = connection.cursor()

    end_date = datetime.date.today()
    start_date = end_date + relativedelta(months=-6)
    end_date = end_date + relativedelta(days=-1)

    cursor.execute(query_fans % (
        brand.id, 
        brand.name, 
        start_date.strftime('%Y%m%d'), 
        end_date.strftime('%Y%m%d'),
        ))

    data = {
        u'socialnetwork': {},
        u'evolution': {
            u'categories': [],
            u'series': {
                u'facebook': [],
                u'twitter': [],
                u'youtube': [],
                },
            },
        u'interaction': {
            u'categories': [],
            u'series':{
                u'facebook': [],
                u'twitter': [],
                u'youtube': [],
                },
            },
        }

    for row in cursor.fetchall():
        data[u'socialnetwork'][row[0]] = human_format(row[2])

    for month in xrange(7):
        date = start_date + relativedelta(months=+month)
        data[u'evolution'][u'categories'].append(date)

        # evolution by month
        try:
            data[u'evolution'][u'series'][u'facebook'].append(
                EvolutionFacebookPageLike.objects.filter(
                    facebook_page__brandfacebookpage__brand=brand,
                    date__month=date.month,
                    date__year=date.year,
                    ).order_by('-date')[0].likes)
        except Exception, e:
            data[u'evolution'][u'series'][u'facebook'].append(0)

        try:
            data[u'evolution'][u'series'][u'twitter'].append(
                EvolutionTwitterProfile.objects.filter(
                    twitter_profile__brandtwitterprofile__brand=brand,
                    date__month=date.month,
                    date__year=date.year,
                    ).order_by('-date')[0].followers_count)
        except Exception, e:
            data[u'evolution'][u'series'][u'twitter'].append(0)

        try:
            data[u'evolution'][u'series'][u'youtube'].append(
                EvolutionYoutubeChannel.objects.filter(
                    youtube_channel__brandyoutubechannel__brand=brand,
                    date__month=date.month,
                    date__year=date.year,
                    ).order_by('-date')[0].subscribers_count)
        except Exception, e:
            data[u'evolution'][u'series'][u'youtube'].append(0)


    start_date = end_date + relativedelta(days=-30)
    cursor.execute(query_interactions % (
        brand.id, 
        brand.name, 
        start_date.strftime('%Y%m%d'), 
        end_date.strftime('%Y%m%d'),
        ))

    for row in cursor.fetchall():
        data[u'interaction'][u'categories'].append(u'%s/%s/%s' % (row[3], row[2], row[1]))
        data[u'interaction'][u'series'][u'facebook'].append(row[4])
        data[u'interaction'][u'series'][u'twitter'].append(row[5])
        data[u'interaction'][u'series'][u'youtube'].append(row[6])

    return render_to_response('customer.html',
                              {'dash_id': dash_id,
                               'brand': brand,
                               'data': data,},
                              context_instance=RequestContext(request))