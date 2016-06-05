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
''':mod:`register_node_with_dataone`
====================================

:Synopsis: Register a new Member Node with DataONE.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import optparse
import sys

# D1.
import d1_client.cnclient

# Django.
from django.core.management.base import NoArgsCommand
from django.conf import settings

# App.
import mn.models
import mn.node


class Command(NoArgsCommand):
  option_list = NoArgsCommand.option_list + (
    optparse.make_option(
      '--update',
      action='store_true',
      dest='update',
      default=False,
      help='Update an existing Node document'
    ),
    optparse.make_option(
      '--view',
      action='store_true',
      dest='view',
      default=False,
      help='Only view generated Node document'
    ),
  )

  help = 'Register a new GMN instance with DataONE'

  def handle_noargs(self, **options):
    self.log_setup()

    logging.info('Running management command: ' 'registe_node_with_dataone')

    verbosity = int(options.get('verbosity', 1))

    self.set_verbosity(verbosity)

    if options['view']:
      self.view()
    elif options['update']:
      self.update()
    else:
      self.register()

  def register(self):
    node = self.generate_node_doc()
    client = self.create_client()
    response = client.registerResponse(node)
    logging.info('Server response:\n{0}'.format(response.read()))
    if response.status == 200:
      logging.info('SUCCESSFUL REGISTRATION')
    else:
      logging.info('REGISTRATION FAILED')

  def update(self):
    node = self.generate_node_doc()
    client = self.create_client()
    response = client.updateNodeCapabilitiesResponse(settings.NODE_IDENTIFIER, node)
    logging.info('Server response:\n{0}'.format(response.read()))

  def view(self):
    node = self.generate_node_doc()
    logging.info('{0}'.format(node.toDOM().toprettyxml(indent='  ')))

  def generate_node_doc(self):
    n = mn.node.Node()
    return n.get()

  def create_client(self):
    client = d1_client.cnclient.CoordinatingNodeClient(
      settings.DATAONE_ROOT,
      cert_path=settings.CLIENT_CERT_PATH,
      key_path=settings.CLIENT_CERT_PRIVATE_KEY_PATH
    )
    return client

  def log_setup(self):
    # Set up logging.
    # We output everything to both file and stdout.
    logging.getLogger('').setLevel(logging.DEBUG)
    formatter = logging.Formatter(
      '%(asctime)s %(levelname)-8s %(name)s %(module)s %(message)s', '%Y-%m-%d %H:%M:%S'
    )
    # Console.
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(formatter)
    logging.getLogger('').addHandler(console_logger)

  def set_verbosity(self, verbosity):
    if verbosity > 0:
      logging.getLogger('').setLevel(logging.DEBUG)
    else:
      logging.getLogger('').setLevel(logging.INFO)
