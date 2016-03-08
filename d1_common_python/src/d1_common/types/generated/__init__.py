#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: __init__.py

:Synopsis:

:Author:
    servilla
  
:Created:
    3/7/16
"""

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y%m%d-%H:%M:%S')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('__init__.py')

__author__ = "servilla"


def main():
    return 0


if __name__ == "__main__":
    main()