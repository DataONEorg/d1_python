#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Generate PyXB binding classes from schemas
"""

import optparse
import os
import sys


def main():
  # Command line options.
  parser = optparse.OptionParser()
  parser.add_option(
    '--schemas', dest='schema_dir', action='store', type='string',
    default='./d1_common/types/schemas'
  )
  parser.add_option(
    '--bindings', dest='binding_dir', action='store', type='string',
    default='./d1_common/types/generated'
  )

  (options, args) = parser.parse_args()

  if not os.path.exists(options.schema_dir):
    print('Could not find the schema folder: {}'.format(options.schema_dir))
    print('This script should be run from ./lib_common/src')
    exit()

  if not os.path.exists(options.binding_dir):
    print((
      'Could not find the bindings destination folder: {}'.
      format(options.schema_dir)
    ))
    print('This script should be run from ./lib_common/src')
    exit()

  g = GenerateBindings(options.schema_dir, options.binding_dir)

  # Generate bindings for 1.0. Also create a types archive for use by the the
  # 1.1 bindings.
  g.generate_bindings([
    '--schema-location=dataoneTypes.xsd',
    '--module=dataoneTypes_v1',
    '--archive-to-file dataoneTypes.wxs',
    '--schema-stripped-prefix='
    '\'https://repository.dataone.org/software/cicore/branches/D1_SCHEMA_V1/\'',
  ])

  # Generate additional bindings for 1.1. Pull 1.0 dependencies from archive.
  g.generate_bindings([
    '--schema-location=dataoneTypes_v1.1.xsd',
    '--module=dataoneTypes_v1_1',
    '--archive-path .:+',
    '--schema-stripped-prefix='
    '\'https://repository.dataone.org/software/cicore/branches/D1_SCHEMA_v1.1/\'',
  ])

  # Generate additional bindings for 2.0. Pull 1.1 dependencies from archive.
  g.generate_bindings([
    '--schema-location=dataoneTypes_v2.0.xsd',
    '--module=dataoneTypes_v2_0',
    '--archive-path .:+',
    '--schema-stripped-prefix='
    '\'https://repository.dataone.org/software/cicore/branches/D1_SCHEMA_v2.0/\'',
  ])

  # g.generate_bindings([
  #  '--schema-location=dataoneErrors.xsd',
  #  '--module=dataoneErrors',
  #  '--archive-path .:+',
  #  '--schema-stripped-prefix='
  #   '\'https://repository.dataone.org/software/cicore/branches/D1_SCHEMA_v2.0/\'',
  # ])

  # Generate bindings for the exception types.
  g.generate_bindings([
    '--schema-location=dataoneErrors.xsd',
    '--module=dataoneErrors',
  ])


# Generate version text files for the bindings, using the Subversion
# revision numbers from the schema files.
#g = GenerateVersionFile(options.schema_dir, options.binding_dir)
#g.generate_version_file('dataoneTypes.xsd', 'dataoneTypes')
#g.generate_version_file('dataoneTypes_v1.1.xsd', 'dataoneTypes_1_1')
#g.generate_version_file('dataoneTypes_v2.0.xsd', 'dataoneTypes_2_0')
#g.generate_version_file('dataoneErrors.xsd', 'dataoneErrors')

#===============================================================================


class GenerateBindings(object):
  def __init__(self, schema_dir, binding_dir):
    self.schema_dir = schema_dir
    self.binding_dir = binding_dir

  def generate_bindings(self, args):
    pyxbgen_args = []
    pyxbgen_args.append('--schema-root=\'{}\''.format(self.schema_dir))
    pyxbgen_args.append('--binding-root=\'{}\''.format(self.binding_dir))
    pyxbgen_args.append(
      '--schema-stripped-prefix='
      '\'https://repository.dataone.org/software/cicore/branches/D1_SCHEMA_v1.1/\''
    )
    pyxbgen_args.extend(args)

    self.run_pyxbgen(pyxbgen_args)

  def run_pyxbgen(self, args):
    cmd = 'pyxbgen {}'.format(' '.join(args))
    print(cmd)
    os.system(cmd)


#===============================================================================


class GenerateVersionFile(object):
  def __init__(self, schema_dir, binding_dir):
    self.schema_dir = schema_dir
    self.binding_dir = binding_dir

  def generate_version_file(self, schema_filename, binding_filename):
    """Given a DataONE schema, generates a file that contains version
    information about the schema.
    """
    version_filename = binding_filename + '_version.txt'
    version_path = os.path.join(self.binding_dir, version_filename)
    schema_path = os.path.join(self.schema_dir, schema_filename)
    try:
      tstamp, svnpath, svnrev, version = self.get_version_info_from_svn(
        schema_path
      )
    except TypeError:
      pass
    else:
      self.write_version_file(version_path, tstamp, svnpath, svnrev, version)

  def write_version_file(
      self, version_file_path, tstamp, svnpath, svnrev, version
  ):
    txt = """# This file is automatically generated. Manual edits will be erased.

# When this file was generated
TIMESTAMP="{}"

# Path of the schema used in the repository
SVNPATH="{1}"

# SVN revision of the schema that was used
SVNREVISION="{2}"

# The version tag of the schema
VERSION="{3}"
""".format(tstamp, svnpath, svnrev, version)

    with open(version_file_path, 'w') as f:
      f.write(txt)


if __name__ == '__main__':
  sys.exit(main())
