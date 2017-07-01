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
"""Update the System Metadata for objects on this GMN instance by copying
specified elements from external SystemMetadata XML documents.

This command is useful in various testing and debugging scenarios but should not
be needed and cannot be safely used on a production node.

The source SystemMetadata is either an XML file or root directory referenced by
--root or an object on a remote node, referenced by --baseurl.

When --root is a root directory or when using --baseurl, a bulk operation is
performed where all discovered objects are matched up with local objects by PID.
The specified elements are then copied from the discovered object to the
matching local object.

Any discovered objects that do not have a local matching PID are ignored. A
regular expression can also be specified to ignore discovered objects even when
there are matching local objects.

Only elements that are children of root are supported. See
SYSMETA_ROOT_CHILD_LIST.

If a discovered object does not have an element that has been specified for
copy, the element is removed from the local object.
"""

from __future__ import absolute_import

import argparse
import logging
import re

import d1_gmn.app.auth
# noinspection PyProtectedMember
import d1_gmn.app.management.commands._util as util
import d1_gmn.app.models
import d1_gmn.app.node
import d1_gmn.app.revision
import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.app.views.asserts
import d1_gmn.app.views.diagnostics

import d1_common.file_iterator
import d1_common.system_metadata
import d1_common.type_conversions
import d1_common.types.exceptions
import d1_common.util
import d1_common.xml

# noinspection PyClassHasNoInit,PyProtectedMember
import d1_test
import d1_test.sample

import d1_client.cnclient
import d1_client.iter.sysmeta_multi
import d1_client.mnclient_2_0

import django.conf
import django.core.management.base


class Command(django.core.management.base.BaseCommand):
  def __init__(self, *args, **kwargs):
    super(Command, self).__init__(*args, **kwargs)
    self._events = d1_common.util.EventCounter()

  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument(
      '--debug', action='store_true', help='debug level logging'
    )
    parser.add_argument(
      '--root', default=None,
      help='path to source SystemMetadata XML file or root of dir tree'
    )
    parser.add_argument(
      '--baseurl', default=None,
      help='base url to node holding source documents'
    )
    parser.add_argument(
      '--pidrx', default=False, help='regex pattern for PIDs to process'
    )
    parser.add_argument(
      'element', default=None, nargs='+',
      choices=d1_common.system_metadata.SYSMETA_ROOT_CHILD_LIST,
      help='one or more elements to update'
    )
    parser.add_argument(
      '--cert-pub', dest='cert_pem_path', action='store', default=None,
      help='path to PEM formatted public key of certificate'
    )
    parser.add_argument(
      '--cert-key', dest='cert_key_path', action='store', default=None,
      help='path to PEM formatted private key of certificate'
    )

  def handle(self, *args, **opt):
    util.log_setup(opt['debug'])
    logging.info(
      u'Running management command: {}'.format(__name__) # util.get_command_name())
    )
    util.exit_if_other_instance_is_running(__name__)
    self._check_debug_mode()
    if opt['root'] and opt['baseurl']:
      raise django.core.management.base.CommandError(
        '--root and --baseurl are mutually exclusive'
      )
    if not (opt['root'] or opt['baseurl']):
      raise django.core.management.base.CommandError(
        'Must specify --root or --baseurl'
      )
    if not (opt['element']):
      raise django.core.management.base.CommandError(
        'Must specify at least one element to copy'
      )
    try:
      self._handle(opt)
    except d1_common.types.exceptions.DataONEException as e:
      raise django.core.management.base.CommandError(str(e))

  def _handle(self, opt):
    try:
      self._update_sysmeta(
        opt['root'], opt['baseurl'], opt['pidrx'], opt['element'],
        opt['cert_pem_path'], opt['cert_key_path']
      )
    except django.core.management.base.CommandError as e:
      logging.error(str(e))
    self._events.log()

  def _check_debug_mode(self):
    if not django.conf.settings.DEBUG_GMN:
      raise django.core.management.base.CommandError(
        'This command is only available when DEBUG_GMN is True in '
        'settings.py'
      )

  def _update_sysmeta(
      self, sysmeta_path, base_url, pid_rx, element_list, cert_pem_path,
      cert_key_path
  ):
    for i, discovered_sysmeta_pyxb in enumerate(
        self._discovered_sysmeta_iter(
          sysmeta_path, base_url, cert_pem_path, cert_key_path
        )
    ):
      self._events.count('SystemMetadata objects discovered')
      pid = d1_common.xml.uvalue(discovered_sysmeta_pyxb.identifier)
      if pid_rx and not re.search(pid_rx, pid):
        skip_msg = 'Skipped: --pidrx mismatch'
        self._events.count(skip_msg)
        logging.info('{}: {}'.format(skip_msg, pid))
        continue

      if not d1_gmn.app.sysmeta.is_pid_of_existing_object(pid):
        skip_msg = 'Skipped: Unknown on local node'
        self._events.count(skip_msg)
        logging.info('{}: {}'.format(skip_msg, pid))
        continue

      before_sysmeta_pyxb = d1_gmn.app.sysmeta.model_to_pyxb(pid)
      sysmeta_pyxb = d1_gmn.app.sysmeta.model_to_pyxb(pid)
      logging.info('Updating: {}'.format(pid))
      d1_common.system_metadata.update_elements(
        sysmeta_pyxb, discovered_sysmeta_pyxb, element_list
      )
      d1_gmn.app.sysmeta.create_or_update(sysmeta_pyxb)
      logging.debug(
        d1_test.sample.get_sxs_diff(before_sysmeta_pyxb, sysmeta_pyxb)
      )
      self._events.count('Updated')

  def _discovered_sysmeta_iter(
      self, sysmeta_path, base_url, cert_pem_path, cert_key_path
  ):
    if sysmeta_path:
      return self._discovered_sysmeta_file_iter(sysmeta_path)
    else:
      return d1_client.iter.sysmeta_multi.SystemMetadataIteratorMulti(
        base_url, client_dict={
          'cert_pem_path': cert_pem_path,
          'cert_key_path': cert_key_path,
        }, list_objects_dict={}
      )

  def _discovered_sysmeta_file_iter(self, sysmeta_path):
    for xml_path in d1_common.file_iterator.file_iter(
        path_list=[sysmeta_path],
        include_glob_list=['*.xml'],
    ):
      try:
        with open(xml_path, 'rb') as f:
          obj_pyxb = d1_common.xml.deserialize(f.read())
      except (EnvironmentError, ValueError):
        # logging.debug('Unable to read or parse. path="{}" err="{}"'.format(xml_path,str(e)))
        continue
      pyxb_type_str = d1_common.type_conversions.get_pyxb_type(obj_pyxb)
      if pyxb_type_str != 'SystemMetadata':
        # logging.debug('Not SystemMetadata. type="{}"'.format(pyxb_type_str))
        continue
      yield obj_pyxb
