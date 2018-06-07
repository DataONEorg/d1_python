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
"""Database model utilities

These are in a separate module because module classes can only be referenced in
an active Django context. More general utilities can be used without an active
context.

Importing this module outside of Django context raises
django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
"""
import logging

import d1_gmn.app
import d1_gmn.app.models


def get_sci_model(pid):
  return d1_gmn.app.models.ScienceObject.objects.get(pid__did=pid)


def get_pids_for_all_locally_stored_objects():
  return d1_gmn.app.models.ScienceObject.objects.all().values_list(
    'pid__did', flat=True
  )


def delete_unused_subjects():
  """Delete any unused subjects from the database. This is not strictly required
  as any unused subjects will automatically be reused if needed in the future.
  """
  # This causes Django to create a single join (check with query.query)
  query = d1_gmn.app.models.Subject.objects.all()
  query = query.filter(scienceobject_submitter__isnull=True)
  query = query.filter(scienceobject_rights_holder__isnull=True)
  query = query.filter(eventlog__isnull=True)
  query = query.filter(permission__isnull=True)
  query = query.filter(whitelistforcreateupdatedelete__isnull=True)

  logging.debug('Deleting {} unused subjects:'.format(query.count()))
  for s in query.all():
    logging.debug('  {}'.format(s.subject))

  query.delete()
