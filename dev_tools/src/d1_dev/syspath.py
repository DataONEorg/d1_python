#!/usr/bin/env python

import sys

# path[0], is the directory containing the script that was used to invoke the Python interpreter
for s in sorted(sys.path[1:]):
  print s
