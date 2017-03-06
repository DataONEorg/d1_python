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

import app.models


def create_id_model(did):
  """Create a new SID or PID.

  Preconditions:
  - {did} is verified to be unused. E.g., with app.views.asserts.is_unused().
  """
  id_model = app.models.IdNamespace()
  id_model.did = did
  id_model.save()
  return id_model


def get_sci_model(pid):
  return app.models.ScienceObject.objects.get(pid__did=pid)


def get_value(sysmeta_pyxb, sysmeta_attr):
  """PyXB validation will fail if required elements are missing. Optional
  elements that are not present are represented with attributes
  that are present but set to None."""
  try:
    return getattr(sysmeta_pyxb, sysmeta_attr).value()
  except (ValueError, AttributeError):
    return None
