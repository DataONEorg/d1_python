#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  :mod:`sys_log` -- System Logging
===================================

:module: sys_log
:platform: Linux
:synopsis: System Logging

.. moduleauthor:: Roger Dahl
"""

from logging import *
import settings

# Set up logging.
getLogger('').setLevel(DEBUG)
formatter = Formatter('%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S')
file_logger = FileHandler(settings.LOG_PATH, 'a')
file_logger.setFormatter(formatter)
getLogger('').addHandler(file_logger)
