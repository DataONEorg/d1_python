#!/usr/bin/env python

# Generate PyXB binding classes from schemas.

import os
import sys
import glob
import optparse


def main():
  # Command line opts.
  parser = optparse.OptionParser()
  # The default location for the schemas relative to d1_common_python if both were checked out as part of cicore.
  parser.add_option(
    '-s',
    '--schemas',
    dest='schema_path',
    action='store',
    type='string',
    default='../../d1_schemas/'
  )
  parser.add_option(
    '-t',
    '--types',
    dest='types_generated_path',
    action='store',
    type='string',
    default='./d1_common/types/generated'
  )

  (opts, args) = parser.parse_args()

  if not os.path.exists(opts.types_generated_path):
    print 'This script should be run from ./d1_common_python/src'
    exit()

  args = []

  args.append('--binding-root=\'{0}\''.format(opts.types_generated_path))
  args.append(
    '--location-prefix-rewrite=\'https://repository.dataone.org/software/cicore/trunk/schemas/=./\''
  )

  for xsd in glob.glob(os.path.join(opts.schema_path, '*.xsd')):
    if os.path.basename(xsd) not in ('dataoneTypes.xsd'):
      continue
    args.append(
      '-u \'{0}\' -m \'{1}\''.format(
        xsd, os.path.splitext(
          os.path.basename(xsd)
        )[0]
      )
    )

  if len(args) <= 2:
    print 'Didn\'t find any schemas at \'{0}\''.format(opts.schema_path)
    exit()

  cmd = 'pyxbgen {0}'.format(' '.join(args))
  print(cmd)
  os.system(cmd)


if __name__ == '__main__':
  main()
