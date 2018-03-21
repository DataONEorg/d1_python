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
"""Utilities for working with revision / obsolescence chains
"""

import d1_common.util
import d1_common.xml


def get_identifiers(sysmeta_pyxb):
  """Return: (pid, sid, obsoletes_pid, obsoleted_by_pid)
  """
  pid = d1_common.xml.get_opt_val(sysmeta_pyxb, 'identifier')
  sid = d1_common.xml.get_opt_val(sysmeta_pyxb, 'seriesId')
  obsoletes_pid = d1_common.xml.get_opt_val(sysmeta_pyxb, 'obsoletes')
  obsoleted_by_pid = d1_common.xml.get_opt_val(sysmeta_pyxb, 'obsoletedBy')
  return pid, sid, obsoletes_pid, obsoleted_by_pid


def topological_sort(unsorted_dict):
  """Sort objects by dependency

  {unconnected_dict} is a dict of PID to obsoleted PID.

  Return:
    sorted_list: A list of PIDs ordered so that all PIDs that obsolete an object
    are listed after the object they obsolete.
    unconnected_dict: A dict of PID to obsoleted PID of any objects that could not
    be added to a revision chain.

  {obsoletes_dict} is modified by the sort and on return holds any items that
  could not be sorted. These items will have obsoletes PIDs that directly or
  indirectly reference a PID that could not be sorted.

  The sort works by repeatedly iterating over an unsorted list of PIDs and
  moving PIDs to the sorted list as they become available. A PID is available to
  be moved to the sorted list if it does not obsolete a PID or if the PID it
  obsoletes is already in the sorted list.
  """
  sorted_list = []
  sorted_set = set()
  found = True
  unconnected_dict = unsorted_dict.copy()
  while found:
    found = False
    for pid, obsoletes_pid in list(unconnected_dict.items()):
      if obsoletes_pid is None or obsoletes_pid in sorted_set:
        found = True
        sorted_list.append(pid)
        sorted_set.add(pid)
        del unconnected_dict[pid]
  return sorted_list, unconnected_dict


def get_pids_in_revision_chain(client, did):
  """Given a SID or a PID of any object in a chain, return a list of all PIDs in
  the chain. The returned list is in the same order as the chain. The initial
  PID is typically obtained by resolving a SID. If the given PID is not in a
  chain, a list containing the single object is returned.
  """

  def req(p):
    return d1_common.xml.get_req_val(p)

  def opt(p, a):
    return d1_common.xml.get_opt_val(p, a)

  sysmeta_pyxb = client.getSystemMetadata(did)
  # Walk to tail
  while opt(sysmeta_pyxb, 'obsoletes'):
    sysmeta_pyxb = client.getSystemMetadata(opt(sysmeta_pyxb, 'obsoletes'))
  chain_pid_list = [req(sysmeta_pyxb.identifier)]
  # Walk from tail to head, recording traversed PIDs
  while opt(sysmeta_pyxb, 'obsoletedBy'):
    sysmeta_pyxb = client.getSystemMetadata(opt(sysmeta_pyxb, 'obsoletedBy'))
    chain_pid_list.append(req(sysmeta_pyxb.identifier))
  return chain_pid_list


def revision_list_to_obsoletes_dict(revision_list):
  return {
    pid: obsoletes_pid
    for pid, sid, obsoletes_pid, obsoleted_by_pid in revision_list
  }


def revision_list_to_obsoleted_by_dict(revision_list):
  return {
    pid: obsoleted_by_pid
    for pid, sid, obsoletes_pid, obsoleted_by_pid in revision_list
  }
