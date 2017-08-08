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

from __future__ import absolute_import

import os
import shutil
import urlparse

import d1_gmn.app.models
import d1_gmn.app.revision
import d1_gmn.app.util

import d1_common.util

import django.apps
import django.conf


def delete_sciobj(pid):
  sciobj = d1_gmn.app.models.ScienceObject.objects.get(pid__did=pid)
  url_split = urlparse.urlparse(sciobj.url)
  delete_sciobj_from_filesystem(url_split, pid)
  delete_sciobj_from_database(pid)
  return pid


def delete_all():
  delete_all_sciobj_from_filesystem()
  delete_all_from_db()


def delete_all_from_db():
  """Clear the database. Used for testing and debugging.
  """
  # The models.CASCADE property is set on all ForeignKey fields, so tables can
  # be deleted in any order without breaking constraints.
  for model in django.apps.apps.get_models():
    model.objects.all().delete()
  # mn.models.IdNamespace.objects.filter(did=pid).delete()
  # The SysMeta object is left orphaned in the filesystem to be cleaned by an
  # asynchronous process later. If the same object that was just deleted is
  # recreated, the old SysMeta object will be overwritten instead of being
  # cleaned up by the async process.
  #
  # This causes associated permissions to be deleted, but any subjects
  # that are no longer needed are not deleted. The orphaned subjects should
  # not cause any issues and will be reused if they are needed again.


def delete_all_sciobj_from_filesystem():
  if os.path.exists(django.conf.settings.OBJECT_STORE_PATH):
    shutil.rmtree(django.conf.settings.OBJECT_STORE_PATH)
  d1_common.util.create_missing_directories_for_file(
    django.conf.settings.OBJECT_STORE_PATH
  )


def delete_sciobj_from_filesystem(url_split, pid):
  if url_split.scheme == 'file':
    sciobj_path = d1_gmn.app.util.get_sciobj_file_path(pid)
    try:
      os.unlink(sciobj_path)
    except EnvironmentError:
      pass


def delete_sciobj_from_database(pid):
  sciobj_model = d1_gmn.app.util.get_sci_model(pid)
  if d1_gmn.app.revision.is_in_revision_chain(sciobj_model):
    d1_gmn.app.revision.cut_from_chain(sciobj_model)
  d1_gmn.app.revision.delete_chain(pid)
  # The models.CASCADE property is set on all ForeignKey fields, so most object
  # related info is deleted when deleting the IdNamespace "root".
  d1_gmn.app.models.IdNamespace.objects.filter(did=pid).delete()
  d1_gmn.app.util.delete_unused_subjects()
