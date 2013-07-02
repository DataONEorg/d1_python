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

from StringIO import StringIO

def generateFolderHelpText(folder):
  '''Generates a human readable description of the folder in rst format.
  '''
  res = StringIO()
  t = u"Description of Folder %s" % folder.name
  res.write(t + u"\n")
  res.write(u"=" * len(t))
  res.write(u"\n\n")
  res.write(u"""The content present in workspace folders is determined by a list 
of specific identifiers and by queries applied against the DataONE search index.
""")
  res.write("\n\n")
  res.write(u"**Queries**\n")
  res.write(u"\n")
  if len(folder.query) > 0:
    for query in folder.query:
      res.write(u"* ``%s``\n" % query)
  else:
    res.write(u"No queries specified at this level.\n") 
  res.write(u"\n\n")
  res.write(u"**Identifiers**\n")
  res.write(u"\n")
  if len(folder.identifier) > 0:
    for pid in folder.identifier:
      res.write(u"* ``%s``\n" % pid)
  else:
    res.write(u"No individual identifiers selected at this level.\n") 
  res.write(u"\n\n")
  res.write(u"**Sub-folders**\n")
  res.write(u"\n")
  if len(folder.folder) > 0:
    for f in folder.folder:
      res.write(u"* ``%s``\n" % f.name)
  else:
    res.write(u"No workspace sub-folders are specified at this level.\n") 
  text = res.getvalue()
  return text.encode('utf8')

