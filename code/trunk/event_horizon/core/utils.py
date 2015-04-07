#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from django.conf import settings


class BulkInsertOrUpdate(object):

    """

    Class to bulk insert or update.
    When we had so many data rows we need to bulk insert with MERGE command.
    In this case, it only works on SQL Server

    """

    def __init__(self, fields, *args, **kwargs):

        self.fields = fields

        # load files
        filename_create = os.path.join(
            settings.PROJECT_ROOT_PATH, 'queries', 'bulk_create.sql')
        filename_insert = os.path.join(
            settings.PROJECT_ROOT_PATH, 'queries', 'bulk_insert.sql')
        filename_merge = os.path.join(
            settings.PROJECT_ROOT_PATH, 'queries', 'bulk_merge.sql')

        try:
            with open(filename_create) as f:
                lines = f.readlines()
            self.query_create = ''.join(lines)

            with open(filename_insert) as f:
                lines = f.readlines()
            self.query_insert = ''.join(lines)

            with open(filename_merge) as f:
                lines = f.readlines()
            self.query_merge = ''.join(lines)
        except IOError:
            print u'There is some errors in query files'
            raise

    def command_bulk_create(self):
        query = u', '.join([u'%s %s' % (field, tp) for field, tp in self.fields.iteritems()])
        return self.query_create % query

    def command_bulk_insert(self, rows):
        query = u'; '.join([u'INSERT #bulk_table VALUES %s' % unicode(row) for row in rows])
        return self.query_insert % query

    def command_bulk_merge(self, destination, matches, update_fields, insert_fields):
        query_match = u''
        for match in matches:
            if match[u'clause']:
                query_match += u' %s destination.%s %s origin.%s' % (
                    match[u'clause'],
                    match[u'first_field'],
                    match[u'comparison'],
                    match[u'second_field']
                    )
            else:
                query_match += u'destination.%s %s origin.%s' % (
                    match[u'first_field'],
                    match[u'comparison'],
                    match[u'second_field']
                    )

        query_update = u', '.join([u'%s = origin.%s' % (field, field) for field in update_fields])
        query_update += u', updated_at = GETDATE()'

        query_insert_destination = u', '.join([u'%s' % f for f in self.fields])
        query_insert_destination += u', created_at, updated_at, deleted'
        query_insert_destination = u'(%s)' % query_insert_destination

        query_insert_origin = u', '.join([u'origin.%s' % f for f in self.fields])
        query_insert_origin += u', GETDATE(), GETDATE(), 0'
        query_insert_origin = u'(%s)' % query_insert_origin

        return self.query_merge % (
            destination,
            query_match,
            query_update,
            query_insert_destination,
            query_insert_origin
            )

    def command_drop_action_table(self):
        return u'DROP TABLE #action_table ;'

    def command_select_action_table(self):
        return u'SELECT * FROM #action_table ;'

    def bulk(self, *args):
        return u' '.join([a for a in args])


