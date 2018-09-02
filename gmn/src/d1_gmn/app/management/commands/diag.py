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
"""This module contains management commands that may be useful in various
testing and debugging scenarios but should not be needed and cannot be safely
used on a production node.
"""

import argparse
import logging
import re

import d1_gmn.app.auth
import d1_gmn.app.delete
# noinspection PyProtectedMember
import d1_gmn.app.did
import d1_gmn.app.management.commands._util as util
import d1_gmn.app.models
import d1_gmn.app.node
import d1_gmn.app.revision
import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.app.views.assert_db

import d1_common.iter.dir
import d1_common.iter.file
import d1_common.system_metadata
import d1_common.type_conversions
import d1_common.types.exceptions
import d1_common.util
import d1_common.xml

import d1_test
import d1_test.sample

import d1_client.cnclient
import d1_client.cnclient_2_0
import d1_client.iter.sysmeta_multi
import d1_client.mnclient_2_0

import django.conf
import django.core.management.base


# noinspection PyClassHasNoInit
class Command(django.core.management.base.BaseCommand):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._command_class_map = {
      'cleardb': ClearDb,
      'exportobj': ExportObjectIdentifiers,
      'updatesysmeta': UpdateSystemMetadata,
    }

    self._events = d1_common.util.EventCounter()

  # TODO: Add getpath command that returns local path of sciobj file in store

  # url(
  #   r'^diag/clear_replication_queue$',
  #   clear_replication_queue,
  #   name='clear_replication_queue',
  # ),

  # url(
  #   r'^diag/delete-event-log$',
  #   delete_event_log,
  #   name='delete_event_log',
  # ),

  # def create_parser(self, prog_name, subcommand):
  #     """
  #     Create and return the ``ArgumentParser`` which will be used to
  #     parse the arguments to this command.
  #     """
  #     parser = django.core.management.base.CommandParser(
  #         self, prog="%s %s" % (os.path.basename(prog_name), subcommand),
  #         description=self.help or None,
  #     )
  #     parser.add_argument('--version', action='version', version=self.get_version())
  #     parser.add_argument(
  #         '-v', '--verbosity', action='store', dest='verbosity', default=1,
  #         type=int, choices=[0, 1, 2, 3],
  #         help='Verbosity level; 0=minimal output, 1=normal output,
  # 2=verbose output, 3=very verbose output',
  #     )
  #     parser.add_argument(
  #         '--settings',
  #         help=(
  #             'The Python path to a settings module, e.g. '
  #             '"myproject.settings.main". If this isn\'t provided, the '
  #             'DJANGO_SETTINGS_MODULE environment variable will be used.'
  #         ),
  #     )
  #     parser.add_argument(
  #         '--pythonpath',
  #         help='A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".',
  #     )
  #     parser.add_argument('--traceback', action='store_true',
  # help='Raise on CommandError exceptions')
  #     parser.add_argument(
  #         '--no-color', action='store_true', dest='no_color',
  #         help="Don't colorize the command output.",
  #     )
  #     self.add_arguments(parser)
  #     return parser

  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument(
      '--debug', action='store_true', help='Debug level logging'
    )
    parser.add_argument(
      'command', choices=sorted(self._command_class_map.keys())
    )

  def handle(self, *args, **opt):
    assert not args
    util.log_setup(opt['debug'])
    try:
      self._handle(opt)
    except d1_common.types.exceptions.DataONEException as e:
      raise django.core.management.base.CommandError(str(e))

  def _handle(self, opt):
    cmd_class = self._command_class_map[opt['command']]
    cmd_obj = cmd_class()
    cmd_obj.run()


class ClearDb(object):
  def __init__(self):
    pass

  # def add_arguments(self, parser):
  #   parser.add_argument(
  #     '--limit', type=int, default=0,
  #     help='Limit number of objects exported. 0 (default) is no limit'
  #   )
  #   parser.add_argument('path', type=str, help='Path to export file')

  def run(self):
    d1_gmn.app.delete.delete_all_from_db()


class ExportObjectIdentifiers(object):
  """Export objects identifiers and related subjects strings to CSV

  The CSV file can be analyzed to determine if objects have the expected
  permissions.

  Permissions are cumulative, so if a subject has, e.g., 'write' permissions on
  an object, 'read' access is implied. So if multiple permissions have been given
  to a subject for an object, only the highest permission is included in the list.
  """

  def add_arguments(self, parser):
    parser.add_argument(
      '--limit', type=int, default=0,
      help='Limit number of objects exported. 0 (default) is no limit'
    )
    parser.add_argument('path', type=str, help='Path to export file')

  def _handle(self, opt):
    logging.info('Exported object list to: {}'.format(opt['path']))
    with open(opt['path'], 'w') as f:
      for i, sciobj_model in enumerate(
          d1_gmn.app.models.ScienceObject.objects.order_by('pid__did')
      ):
        f.write(
          '{}\t{}\n'.format(
            sciobj_model.pid.did, ','.join([
              '{}={}'.format(subj, d1_gmn.app.auth.level_to_action(level))
              for (subj, level) in self.get_object_permissions(sciobj_model)
            ])
          )
        )
        if i + 1 == opt['limit']:
          break

  def get_object_permissions(self, sciobj_model):
    return [
      (p.subject.subject, p.level)
      for p in d1_gmn.app.models.Permission.objects.filter(sciobj=sciobj_model)
      .order_by('subject__subject')
    ]


class UpdateSystemMetadata(object):
  """Update the System Metadata for objects on this GMN instance by copying
  specified elements from external SystemMetadata XML documents.

  The source SystemMetadata is either an XML file or root directory referenced
  by --root or an object on a remote node, referenced by --baseurl.

  When --root is a root directory or when using --baseurl, a bulk operation is
  performed where all discovered objects are matched up with local objects by
  PID. The specified elements are then copied from the discovered object to the
  matching local object.

  Any discovered objects that do not have a local matching PID are ignored. A
  regular expression can also be specified to ignore discovered objects even
  when there are matching local objects.

  Only elements that are children of root are supported. See
  SYSMETA_ROOT_CHILD_LIST.

  If a discovered object does not have an element that has been specified for
  copy, the element is removed from the local object.
  """

  def __init__(self):
    self._events = d1_common.util.EventCounter()

  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument(
      '--root',
      help='Path to source SystemMetadata XML file or root of dir tree'
    )
    parser.add_argument(
      '--baseurl', help='Base url to node holding source documents'
    )
    parser.add_argument(
      '--pidrx', default=False, help='Regex pattern for PIDs to process'
    )
    parser.add_argument(
      'element', nargs='+',
      choices=d1_common.system_metadata.SYSMETA_ROOT_CHILD_LIST,
      help='One or more elements to update'
    )
    parser.add_argument(
      '--cert-pub', dest='cert_pem_path', action='store',
      help='Path to PEM formatted public key of certificate'
    )
    parser.add_argument(
      '--cert-key', dest='cert_key_path', action='store',
      help='Path to PEM formatted private key of certificate'
    )

  def handle(self, *args, **opt):
    util.log_setup(opt['debug'])
    logging.info(
      'Running management command: {}'.format(__name__) # util.get_command_name())
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
    self._events.dump_to_log()

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
      pid = d1_common.xml.get_req_val(discovered_sysmeta_pyxb.identifier)
      if pid_rx and not re.search(pid_rx, pid):
        skip_msg = 'Skipped: --pidrx mismatch'
        self._events.count(skip_msg)
        logging.info('{}: {}'.format(skip_msg, pid))
        continue

      if not d1_gmn.app.did.is_existing_object(pid):
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
    for xml_path in d1_common.iter.dir.dir_iter(
        path_list=[sysmeta_path],
        include_glob_list=['*.xml'],
    ):
      try:
        with open(xml_path, 'rb') as f:
          obj_pyxb = d1_common.xml.deserialize(f.read())
      except (EnvironmentError, ValueError):
        # logging.debug('Unable to read or parse. path="{}" err="{}"'.format(xml_path,str(e)))
        continue
      pyxb_type_str = d1_common.type_conversions.pyxb_get_type_name(obj_pyxb)
      if pyxb_type_str != 'SystemMetadata':
        # logging.debug('Not SystemMetadata. type="{}"'.format(pyxb_type_str))
        continue
      yield obj_pyxb
