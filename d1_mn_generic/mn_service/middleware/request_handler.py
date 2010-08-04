#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
:mod:`request_handler`
=========================

:platform: Linux
:Synopsis:
.. moduleauthor:: Roger Dahl
'''

from django.http import HttpResponse


class request_handler():
  def process_request(self, request):
    print '>' * 80
    print 'Request:'
    print '<' * 80
    return None
