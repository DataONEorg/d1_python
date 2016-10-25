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


import app.models


def create_id_row(did):
  """Create a new SID or PID.

  Preconditions:
  - {did} is verified to be unused. E.g., with view_asserts.is_unused().
  """
  id_row = app.models.IdNamespace()
  id_row.did = did
  id_row.save()
  return id_row


def get_sci_row(pid):
  return app.models.ScienceObject.objects.get(pid__did=pid)


def get_value(sysmeta_obj, sysmeta_attr):
  """PyXB validation will fail if required elements are missing. Optional
  elements that are not present are represented with attributes
  that are present but set to None."""
  try:
    return getattr(sysmeta_obj, sysmeta_attr).value()
  except (ValueError, AttributeError):
    return None

