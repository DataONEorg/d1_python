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
"""Utilities for manipulating Series ID (SID)
"""

from __future__ import absolute_import

# App.
import app.auth
import app.models
import app.util
import app.sysmeta_util


def is_sid(did):
  return app.models.SeriesIdToScienceObject.objects.filter(sid__did=did
                                                           ).exists()


def has_sid(sysmeta_pyxb):
  return get_sid(sysmeta_pyxb) is not None


def get_sid(sysmeta_pyxb):
  return app.sysmeta_util.get_value(sysmeta_pyxb, 'seriesId')


def create_sid(sid, pid):
  """Create a new {sid} that resolves to {pid}.

  Preconditions:
  - {sid} is verified to be unused. E.g., with app.views.asserts.is_unused().
  - {pid} is verified to exist. E.g., with app.views.asserts.is_pid().
  """
  sci_model = app.sysmeta_util.get_sci_model(pid)
  _create_sid(sid, sci_model)


def update_sid(sid, pid):
  """Change the existing {sid} to resolve to {pid}.

  Preconditions:
  - SID is verified to exist. E.g., with app.views.asserts.is_sid().

  Postconditions:
  - The SID maps to the object specified by pid.
  """
  sci_model = app.sysmeta_util.get_sci_model(pid)
  _update_sid(sid, sci_model)


def resolve_sid(sid):
  """Get the PID to which the {sid} currently maps.

  Preconditions:
  - {sid} is verified to exist. E.g., with app.views.asserts.is_sid().
  """
  return app.models.SeriesIdToScienceObject.objects.get(
    sid__did=sid
  ).sciobj.pid.did


def get_sid_by_pid(pid):
  """Get the SID to which the {pid} currently maps.

  Return None if there is no SID that currently maps to {pid}.

  Preconditions:
  - {pid} is verified to exist. E.g., with app.views.asserts.is_pid().
  """
  try:
    return app.models.SeriesIdToScienceObject.objects.get(
      sciobj__pid__did=pid
    ).sid.did
  except app.models.SeriesIdToScienceObject.DoesNotExist:
    return None


#
# Private
#


def _create_sid(sid, sci_model):
  """Create a new {sid} that resolves to {sci_model}."""
  sid_model = app.models.SeriesIdToScienceObject()
  sid_model.sciobj = sci_model
  sid_model.sid = app.models.did(sid)
  sid_model.save()


def _update_sid(sid, sci_model):
  """Change an existing {sid} to resolve to {sci_model}"""
  sid_model = app.models.SeriesIdToScienceObject.objects.get(sid__did=sid)
  sid_model.sciobj = sci_model
  sid_model.save()


# def update_sid(sysmeta_pyxb):
#   pid = sysmeta_pyxb.identifier.value()
#   sci_model = sysmeta_util.get_sci_model(pid)
#   _update_sid(sci_model, sysmeta_pyxb)
#   sci_model.save()

# def move_sid_to_last_object_in_chain(pid):
#   """Move SID to the last object in a chain to which {pid} belongs.
#
#   - If the chain does not have a SID, do nothing.
#   - If the SID already maps to the last object in the chain, do nothing.
#
#   A SID always resolves to the last object in its chain. So System Metadata XML
#   docs are used for introducing SIDs and setting initial mappings, but the
#   database maintains the current mapping going forward.
#
#   Preconditions:
#   - PID is verified to exist. E.g., with app.views.asserts.is_pid().
#
#   Postconditions:
#   - The SID maps to the last object in the chain.
#   """
#   sid = sysmeta_db.get_sid_by_pid(pid)
#   if sid:
#     chain_pid_list = sysmeta_db.get_pids_in_obsolescence_chain(pid)
#     update_sid(sid, chain_pid_list[-1])
