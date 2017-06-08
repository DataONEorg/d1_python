#!/usr/bin/env python

from __future__ import absolute_import

import pstats

p = pstats.Stats('profile')
#p.strip_dirs().sort_stats(-1).print_stats()
p.sort_stats('cumulative').print_stats(10)
