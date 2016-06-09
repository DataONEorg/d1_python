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
'''Module d1_client.svnrevision
===============================

Check subversion revision of the tree in which this file is contained
and returns that value or the statically set value on failure.

:Created: 2010-01-11
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
  - pysvn
'''

import os
import logging
import sys
import codecs

try:
  import pysvn
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: apt-get install python-svn\n')
  sys.stderr.write('See:  http://pysvn.tigris.org/project_downloads.html\n')
  raise

_default_revision = "10035" # TAG


def getSvnRevision(update_static=False):
  '''If update_static then attempt to modify this source file with the current
    svn revision number.
    '''
  rev = _default_revision
  try:
    here = os.path.abspath(os.path.dirname(__file__))
    cli = pysvn.Client()
    rev = str(cli.info(here).revision.number)
    if update_static and rev != _default_revision:
      # Try to update the static revision number - requires file write
      # permission
      try:
        tf = codecs.open(os.path.abspath(__file__), 'r', 'utf-8')
        content = tf.read()
        tf.close()
        content = content.replace(
          u'_default_revision="%s" ##TAG' % _default_revision,
          u'_default_revision="%s" ##TAG' % rev, 1
        )
        logging.info("Setting revision in %s to %s" % (os.path.abspath(__file__), rev))
        tf = codecs.open(os.path.abspath(__file__), 'w', 'utf-8')
        tf.write(content)
        tf.close()
      except Exception as e:
        logging.exception(e)
  except:
    logging.error("pysvn not available for revision information.")
  return rev


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  ver = getSvnRevision(update_static=True)
  print "svn:%s" % ver
