#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models

from social.models import FacebookUser, FacebookPage, InsightsFacebookPage


class PageSave(object):
    
    """
    PageSave
    =========

    PageSave is a class that saves a list of data into model.

    """

    def __init__(self, app, class_name, *args, **kwargs):
        self._app = app
        self._class_name = class_name
        self.responses = []


    def start_save(self, rows, **kwargs):
        app = __import__(self._app)
        cls = getattr(app.models, self._class_name)

        for row in rows:
            response = cls.row_save(row, **kwargs)
            self.responses.append(response)