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
"""Delete science objects and metadata
"""

import urllib.parse

import d1_gmn.app.did
import d1_gmn.app.model_util
import d1_gmn.app.models
import d1_gmn.app.revision
import d1_gmn.app.sciobj_store
import d1_gmn.app.util

import django.apps
import django.conf


def delete_sciobj(pid):
  sciobj = d1_gmn.app.models.ScienceObject.objects.get(pid__did=pid)
  url_split = urllib.parse.urlparse(sciobj.url)
  d1_gmn.app.sciobj_store.delete_sciobj(url_split, pid)
  delete_sciobj_from_database(pid)
  return pid


# def delete_all():
#   d1_gmn.app.sciobj_store.delete_all_sciobj()
#   delete_all_from_db()


def delete_all_from_db():
  """Clear the database. Used for testing and debugging.
  """
  # The models.CASCADE property is set on all ForeignKey fields, so tables can
  # be deleted in any order without breaking constraints.
  for model in django.apps.apps.get_models():
    model.objects.all().delete()


def delete_sciobj_from_database(pid):
  sciobj_model = d1_gmn.app.model_util.get_sci_model(pid)
  if d1_gmn.app.did.is_in_revision_chain(sciobj_model):
    d1_gmn.app.revision.cut_from_chain(sciobj_model)
  d1_gmn.app.revision.delete_chain(pid)
  # The models.CASCADE property is set on all ForeignKey fields, so most object
  # related info is deleted when deleting the IdNamespace "root".
  d1_gmn.app.models.IdNamespace.objects.filter(did=pid).delete()
  d1_gmn.app.model_util.delete_unused_subjects()
