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
"""Utilities shared between the sysmeta modules
"""

from __future__ import absolute_import

import logging

import gmn.app.models


def create_id_model(did):
  """Create a new SID or PID.

  Preconditions:
  - {did} is verified to be unused. E.g., with gmn.app.views.asserts.is_unused().
  """
  id_model = gmn.app.models.IdNamespace()
  id_model.did = did
  id_model.save()
  return id_model


def get_sci_model(pid):
  return gmn.app.models.ScienceObject.objects.get(pid__did=pid)


def get_value(sysmeta_pyxb, sysmeta_attr):
  """Get a Simple Content value from PyXB

  PyXB validation will fail if required elements are missing. Optional elements
  that are not present are represented with attributes that are present but set
  to None."""
  try:
    return uvalue(getattr(sysmeta_pyxb, sysmeta_attr))
  except (ValueError, AttributeError):
    return None


def uvalue(obj_pyxb):
  """Getting a Simple Content value from PyXB with .value() returns a PyXB type
  that lazily evaluates to a native unicode string. This confused parts of the
  Django ORM that check types before passing values to the database. This
  function forces immediate conversion to unicode.
  """
  return unicode(obj_pyxb.value())


def delete_unused_subjects():
  """Delete any unused subjects from the database. This is not strictly required
  as any unused subjects will automatically be reused if needed in the future.
  """
  # This causes Django to create a single join (check with query.query)
  query = gmn.app.models.Subject.objects.all()
  query = query.filter(scienceobject_submitter__isnull=True)
  query = query.filter(scienceobject_rights_holder__isnull=True)
  query = query.filter(eventlog__isnull=True)
  query = query.filter(permission__isnull=True)
  query = query.filter(whitelistforcreateupdatedelete__isnull=True)

  logging.debug('Deleting {} unused subjects:'.format(query.count()))
  for s in query.all():
    logging.debug(u'  {}'.format(s.subject))

  query.delete()
