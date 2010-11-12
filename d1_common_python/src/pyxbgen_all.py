#!/usr/bin/env python

# Generate PyXB binding classes from schemas.

import os
import sys
import glob

try:
  os.mkdir('./pyxb')
except OSError:
  pass

args = []

args.append('--binding-root=\'./pyxb\'')
args.append(
  '--location-prefix-rewrite=\'https://repository.dataone.org/software/cicore/trunk/schemas/=./\''
)

for xsd in glob.glob('*.xsd'):
  if xsd in ('common.xsd', 'dryadMetsAny.xsd', 'dryadXlink.xsd', 'dryadDim.xsd'):
    continue
  args.append('-u \'{0}\' -m \'{1}\''.format(xsd, os.path.splitext(xsd)[0]))

cmd = 'pyxbgen {0}'.format(' '.join(args))
print(cmd)
os.system(cmd)
