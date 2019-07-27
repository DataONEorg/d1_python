# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""Database model utilities.

These are in a separate module because module classes can only be referenced in
an active Django context. More general utilities can be used without an active
context.

Importing this module outside of Django context raises
django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.

"""
import logging

import d1_gmn.app
import d1_gmn.app.models

logger = logging.getLogger(__name__)


def query_sciobj(filter_arg_dict=None):
    """Return a query for iterating over local SciObj.

    Args:
        filter_arg_dict:
    """
    query = d1_gmn.app.models.ScienceObject.objects.filter(**(filter_arg_dict or {}))
    query = query.order_by("modified_timestamp", "id")
    return query


def query_sciobj_count(filter_arg_dict=None):
    """Return a query for iterating over local SciObj.

    Args:
        filter_arg_dict:
    """
    return query_sciobj(filter_arg_dict).count()


def query_sciobj_with_annotate(filter_arg_dict=None, generate_dict=None):
    """Return a query for iterating over local SciObj.

    Args:
        filter_arg_dict:
        generate_dict:
    """
    query = query_sciobj(filter_arg_dict)
    query, annotate_key_list = annotate_query(query, generate_dict or {})
    return query, annotate_key_list


def annotate_query(query, generate_dict):
    """Add annotations to the query to retrieve values required by field value generate
    functions."""
    annotate_key_list = []
    for field_name, annotate_dict in generate_dict.items():
        for annotate_name, annotate_func in annotate_dict["annotate_dict"].items():
            query = annotate_func(query)
            annotate_key_list.append(annotate_name)
    return query, annotate_key_list


def get_sci_model(pid):
    return d1_gmn.app.models.ScienceObject.objects.get(pid__did=pid)


def query_all_sysmeta_backed_sciobj():
    """Get PIDs for all SciObj for which there is locally stored SysMeta. This excludes
    many possible other PIDs. See classify_identifier() for an overview.
    """
    return d1_gmn.app.models.ScienceObject.objects.all()


def count_all_sysmeta_backed_sciobj():
    return query_all_sysmeta_backed_sciobj().count()


def delete_unused_subjects():
    """Delete any unused subjects from the database.

    This is not strictly required as any unused subjects will automatically be reused if
    needed in the future.

    """
    # This causes Django to create a single join (check with query.query)
    query = d1_gmn.app.models.Subject.objects.all()
    query = query.filter(scienceobject_submitter__isnull=True)
    query = query.filter(scienceobject_rights_holder__isnull=True)
    query = query.filter(eventlog__isnull=True)
    query = query.filter(permission__isnull=True)
    query = query.filter(whitelistforcreateupdatedelete__isnull=True)

    logger.debug("Deleting {} unused subjects:".format(query.count()))
    for s in query.all():
        logging.debug("  {}".format(s.subject))

    query.delete()
