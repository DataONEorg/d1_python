#!/usr/bin/env python

import pstats
p = pstats.Stats('profile')
#p.strip_dirs().sort_stats(-1).print_stats()
p.sort_stats('cumulative').print_stats(10)
