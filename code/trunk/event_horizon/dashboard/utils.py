#!/usr/bin/python
# -*- coding: utf-8 -*-


def human_format(num):
    magnitude = 0
    while num >= 1000:  # TODO: handle negative numbers?
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.1f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])