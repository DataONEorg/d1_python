#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`Top level __init__.py`
==============

:Synopsis:
  System Logging is used for logging internal events that are not exposed
  through any of the DataONE interfaces. Used for monitoring service and doing
  post mortem debugging.

.. moduleauthor:: Roger Dahl
"""

#Stdlib.
import logging
import sys

# App.
import settings

# Set up logging.
# We output everything to both file and stdout.
logging.getLogger('').setLevel(logging.DEBUG)
formatter = logging.Formatter(
  '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
)
# Log file.
file_logger = logging.FileHandler(settings.LOG_PATH, 'a')
file_logger.setFormatter(formatter)
logging.getLogger('').addHandler(file_logger)
# Console.
#console_logger = StreamHandler(sys.stdout)
#console_logger.setFormatter(formatter)
#getLogger('').addHandler(console_logger)
