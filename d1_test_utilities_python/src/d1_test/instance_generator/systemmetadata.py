#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2011
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
Module d1_instance_generator.systemmetadata
===========================================

:Synopsis: Generate instance of SystemMetadata using random pieces.
:Created: 2011-07-31
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import codecs
import hashlib
import os
import random
import logging

# 3rd party.
from lxml import etree

# D1.
from d1_common.types.generated import dataoneTypes

# App.
import accesspolicy
import checksum
import dates
import identifier
import random_data
import replica
import replicationpolicy


def generate(options=None):
  '''Generate a random System Metadata object.

  options is a set of key-value pairs that allow the caller to prevent specific
  sections of the System Metadata from being randomly generated by providing
  previously created objects of the appropriate types.

  E.g., providing an Identifier object in options['identifier'] causes that
  object to be used and prevents a randomly generated Identifer from being used.
  '''
  if options is None:
    options = {}
  logging.debug("OPTIONS at sysmeta.generate= %s" % str(options))

  sysmeta = dataoneTypes.systemMetadata()
  sysmeta.serialVersion = random.randint(1, 100)
  sysmeta.identifier = options.get('identifier', identifier.generate(prefix="id_"))
  sysmeta.dateUploaded = options.get('dateUploaded', dates.now())
  sysmeta.formatId = options.get('formatId', 'application/octet-stream')
  sysmeta.checksum = options.get('checksum', checksum.generate())
  sysmeta.size = options.get('size', random.randint(1, 1024**4))
  sysmeta.submitter = options.get(
    'submitter', u'submitter_' + random_data.random_3_words()
  )
  sysmeta.rightsHolder = options.get('rightsHolder',
                                     u'rightsHolder_' + \
                                     random_data.random_3_words())
  sysmeta.originMemberNode = options.get(
    'originMemberNode',
    u"originMemberNode_" + random_data.random_unicode_string_no_whitespace()
  )
  sysmeta.authoritativeMemberNode = options.get('authoritativeMemberNode',
                                                u"authoritativeMemberNode_" + \
      random_data.random_unicode_string_no_whitespace())
  sysmeta.accessPolicy = options.get(
    'accessPolicy',
    accesspolicy.generate(
      min_rules=1, max_rules=5, max_subjects=5
    )
  )
  sysmeta.replicationPolicy = options.get(
    'replicationPolicy', replicationpolicy.generate()
  )
  sysmeta.dateSysMetadataModified = options.get('dateSysMetadataModified', dates.now())
  logging.debug(str(sysmeta.checksum.value()))
  return sysmeta


def generate_from_flo(flo, options=None):
  if options is None:
    options = {}

  options['checksum'] = checksum.generate_from_flo(flo)
  logging.debug("checksum=%s" % options['checksum'].value())
  logging.debug("algorithm=%s" % options['checksum'].algorithm)

  flo.seek(0, os.SEEK_END)
  options['size'] = flo.tell()

  return generate(options)


def generate_from_file(path, options=None):
  if options is None:
    options = {}

  f = open(path, 'rb')
  return generate_from_flo(f, options)
