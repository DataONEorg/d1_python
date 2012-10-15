#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
''':mod:`pyxbgen_all`
=====================

:Synopsis:
 - Generate PyXB binding classes from schemas.
:Author: DataONE (Dahl)
'''

import datetime
import optparse
import os
import xml.etree.ElementTree

try:
  import pysvn
except ImportError:
  print 'Try: sudo apt-get install python-svn'
  raise

# Note: Even if the schema is in multiple files, pyxbgen is still
# run only once, but with multiple sets of -u and -m.


def main():
  # Command line options.
  parser = optparse.OptionParser()
  # The default location for the schemas relative to d1_common_python if both were checked out as part of cicore.
  parser.add_option(
    '--schemas',
    dest='schema_dir',
    action='store',
    type='string',
    default='./d1_schemas'
  )
  parser.add_option(
    '--bindings',
    dest='binding_dir',
    action='store',
    type='string',
    default='./d1_common/types/generated'
  )
  #parser.add_option('--process', dest='process_schemas', action='store', type='string', default='dataoneTypes_v1.1.xsd;dataoneErrors.xsd')
  parser.add_option(
    '--process',
    dest='process_schemas',
    action='store',
    type='string',
    default='dataoneTypes.xsd;dataoneTypes_v1.1.xsd;dataoneErrors.xsd'
  )

  (options, args) = parser.parse_args()

  if not os.path.exists(options.binding_dir):
    print 'The destination folder for the bindings does not exist.'
    print 'This script should be run from ./d1_common_python/src'
    exit()

  schema_groups = options.process_schemas.split(';')

  g = GenerateBindings(options.binding_dir, options.schema_dir)
  g.process_schema_groups(schema_groups)


class GenerateBindings(object):
  def __init__(self, binding_dir, schema_dir):
    self.binding_dir = binding_dir
    self.schema_dir = schema_dir

  def process_schema_groups(self, schema_groups):
    for schema_group_str in schema_groups:
      schema_group = schema_group_str.split(',')
      self.process_schema_group(schema_group)

  def process_schema_group(self, schema_group):
    print 'Processing: {0}'.format(schema_group)
    self.generate_pyxb_bindings_for_schema_group(schema_group)
    self.generate_version_text_files_for_schema_group(schema_group)

  def generate_pyxb_bindings_for_schema_group(self, schema_group):
    pyxbgen_args = []
    #pyxbgen_args.append('--location-prefix-rewrite=\'https://repository.dataone.org/software/cicore/trunk/schemas/={0}/\''.format(self.schema_dir))
    #pyxbgen_args.append('--location-prefix-rewrite=\'https://repository.dataone.org/software/cicore/branches/D1_SCHEMA_v1.1/={0}/\''.format(self.schema_dir))
    pyxbgen_args.append(
      '--schema-stripped-prefix=\'https://repository.dataone.org/software/cicore/branches/D1_SCHEMA_v1.1/\''
    )

    pyxbgen_args.append('--binding-root=\'{0}\''.format(self.binding_dir))

    for schema_filename in schema_group:
      schema_name = os.path.splitext(schema_filename)[0]
      schema_path = os.path.join(self.schema_dir, schema_filename)
      pyxbgen_args.append('--schema-location=\'{0}\''.format(schema_path))
      pyxbgen_args.append('--module=\'{0}\''.format(schema_name.replace('.', '_')))

    binding_path = os.path.join(
      self.binding_dir, os.path.splitext(schema_group[0])[0] + '.py'
    )

    # pyxbgen sometimes does not want to overwrite existing binding classes.
    try:
      os.unlink(binding_path)
    except OSError:
      pass

    self.run_pyxbgen(pyxbgen_args)

  def run_pyxbgen(self, args):
    cmd = 'pyxbgen {0}'.format(' '.join(args))
    print(cmd)
    os.system(cmd)

  def generate_version_text_files_for_schema_group(self, schema_group):
    for schema_filename in schema_group:
      self.generate_version_text_file(schema_filename)

  def generate_version_text_file(self, schema_filename):
    '''Given a DataONE schema, generates a file that contains version
    information about the schema.
    '''
    version_filename = os.path.splitext(schema_filename)[0] + '_version.txt'
    version_path = os.path.join(self.binding_dir, version_filename)
    schema_path = os.path.join(self.schema_dir, schema_filename)
    try:
      tstamp, svnpath, svnrev, version = self.get_version_info_from_svn(schema_path)
    except TypeError:
      pass
    else:
      self.write_version_file(version_path, tstamp, svnpath, svnrev, version)

  def get_version_info_from_svn(self, schema_path):
    print schema_path
    cli = pysvn.Client()
    svninfo = cli.info(schema_path)
    if svninfo is None:
      return
    svnrev = str(svninfo.revision.number)
    svnpath = svninfo.url
    doc = xml.etree.ElementTree.parse(schema_path)
    version = doc.getroot().attrib['version']
    tstamp = datetime.datetime.utcnow().isoformat()
    return tstamp, svnpath, svnrev, version

  def write_version_file(self, version_file_path, tstamp, svnpath, svnrev, version):
    txt = '''# This file is automatically generated. Manual edits will be erased.

# When this file was generated
TIMESTAMP="{0}"

# Path of the schema used in the repository
SVNPATH="{1}"

# SVN revision of the schema that was used
SVNREVISION="{2}"

# The version tag of the schema
VERSION="{3}"
'''.format(tstamp, svnpath, svnrev, version)

    with open(version_file_path, 'w') as f:
      f.write(txt)


if __name__ == '__main__':
  main()
