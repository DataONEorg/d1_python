#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 3rd party source
"""Upgrade all pip managed packages to latest PyPI release
https://github.com/nschloe/pipdated
http://stackoverflow.com/a/3452888/353337
"""

import os
os.system(
  "pip freeze --local | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U"
)
