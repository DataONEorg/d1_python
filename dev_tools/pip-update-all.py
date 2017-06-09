#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 3rd party source
"""Upgrade all pip managed packages to latest PyPI release
https://github.com/nschloe/pipdated
http://stackoverflow.com/a/3452888/353337
"""

from __future__ import absolute_import

import datetime
import os
import sys


def main():
  try:
    os.utime('/usr/', None)
  except EnvironmentError:
    sys.exit('Must be root')

  os.system(
    "pip freeze > pip_freeze_{}.txt"
    .format(datetime.datetime.now().isoformat())
  )

  os.system(
    "pip freeze --local | "
    "grep -v '^\-e' | "
    "cut -d = -f 1 | "
    "xargs -n1 pip install -U"
  )

  os.system("pip check")


if __name__ == '__main__':
  main()
