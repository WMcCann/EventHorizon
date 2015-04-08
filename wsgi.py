#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys 

sys.path.append('C:\inetpub\www.eventhorizon.wmccann.com')
sys.path.append('C:\inetpub\www.eventhorizon.wmccann.com\event_horizon') 

os.environ['DJANGO_SETTINGS_MODULE'] = 'event_horizon.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler() 

import isapi_wsgi
# The entry points for the ISAPI extension.
def __ExtensionFactory__():
    return isapi_wsgi.ISAPISimpleHandler(application)