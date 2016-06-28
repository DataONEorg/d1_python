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
'''
Module d1_common.svnrevision
============================

Check subversion revision of the tree in which this file is contained
and returns that value or the statically set value on failure.

:Created: 2011-02-14
:Author: DataONE (Vieglais)
:Dependencies:
  - python 2.6
'''

import os
import logging

_default_revision = "3492" ##TAG


def getSvnRevision(update_static=False):
  '''If update_static then attempt to modify this source file with the current
  svn revision number.
  '''
  rev = _default_revision
  logger = logging.getLogger('d1_common.getSvnRevision')
  try:
    import pysvn
    here = os.path.abspath(os.path.dirname(__file__))
    cli = pysvn.Client()
    rev = str(cli.info(here).revision.number)
    if update_static and rev != _default_revision:
      #Try to update the static revision number - requires file write permission
      try:
        import codecs
        fname = os.path.abspath(__file__)
        if fname.endswith('.py'):
          logger.error("FILE=%s" % fname)
          tf = codecs.open(fname, 'r', 'utf-8')
          content = tf.read()
          tf.close()
          content = content.replace(u'_default_revision="%s" ##TAG' % \
                                      _default_revision,
                                    u'_default_revision="%s" ##TAG' % rev, 1 )
          logger.info("Setting revision in %s to %s" % \
                         (fname, rev) )
          tf = codecs.open(fname, 'w', 'utf-8')
          tf.write(content)
          tf.close()
      except Exception, e:
        logger.exception(e)
  except:
    logger.error("pysvn not available for revision information.")
  return rev


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  ver = getSvnRevision(update_static=True)
  print "svn:%s" % ver
