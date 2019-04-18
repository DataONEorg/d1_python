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
"""Extract SciObj values from models"""
import d1_gmn.app
import d1_gmn.app.models
import d1_common.util

import django.contrib.postgres.aggregates
import d1_gmn.app.auth
import d1_common.types.exceptions


def extract_values_query(query, field_list, out_stream=None):
    """Get list of dicts where each dict holds values from one SciObj.

    Args:
        field_list: list of str
            List of field names for which to return values. Must be strings from
            FIELD_NAME_TO_generate_dict.keys().

            If None, return all fields.

        filter_arg_dict: dict
            Dict of arguments to pass to ``ScienceObject.objects.filter()``.

        out_stream: open file-like object
            If provided, the JSON doc is streamed out instead of buffered in memory.

    Returns:
        list of dict: The keys in the returned dict correspond to the field names in
        ``field_list``.

    Raises:
        raise d1_common.types.exceptions.InvalidRequest() if ``field_list`` contains any
        invalid field names. A list of the invalid fields is included in the exception.

    """
    lookup_dict, generate_dict = _split_field_list(field_list)

    query, annotate_key_list = _annotate_query(query, generate_dict)
    # return query, annotate_key_list
    #
    # query, annotate_key_list = _create_query(filter_arg_dict, generate_dict)

    lookup_list = [v["lookup_str"] for k, v in lookup_dict.items()] + annotate_key_list

    if out_stream is None:
        return _create_sciobj_list(query, lookup_list, lookup_dict, generate_dict)
    else:
        return _write_stream(query, lookup_list, lookup_dict, generate_dict, out_stream)


def extract_values(field_list=None, filter_arg_dict=None, out_stream=None):
    """Get list of dicts where each dict holds values from one SciObj.

    Args:
        field_list: list of str
            List of field names for which to return values. Must be strings from
            FIELD_NAME_TO_generate_dict.keys().

            If None, return all fields.

        filter_arg_dict: dict
            Dict of arguments to pass to ``ScienceObject.objects.filter()``.

    Returns:
        list of dict: The keys in the returned dict correspond to the field names in
        ``field_list``.

    Raises:
        raise d1_common.types.exceptions.InvalidRequest() if ``field_list`` contains any
        invalid field names. A list of the invalid fields is included in the exception.

    """
    lookup_dict, generate_dict = _split_field_list(field_list)
    query, annotate_key_list = _create_query(filter_arg_dict, generate_dict)

    lookup_list = [v["lookup_str"] for k, v in lookup_dict.items()] + annotate_key_list

    if out_stream is None:
        return _create_sciobj_list(query, lookup_list, lookup_dict, generate_dict)
    else:
        return _write_stream(query, lookup_list, lookup_dict, generate_dict, out_stream)


def _create_sciobj_list(query, lookup_list, lookup_dict, generate_dict):
    sciobj_list = []
    for sciobj_value_list in query.values_list(*lookup_list):
        sciobj_list.append(
            _value_list_to_sciobj_dict(
                sciobj_value_list, lookup_list, lookup_dict, generate_dict
            )
        )
    return sciobj_list


def _write_stream(query, lookup_list, lookup_dict, generate_dict, out_stream):
    out_stream.write("[\n")
    for sciobj_value_list in query.values_list(*lookup_list):
        json_str = d1_common.util.serialize_to_normalized_pretty_json(
            _value_list_to_sciobj_dict(
                sciobj_value_list, lookup_list, lookup_dict, generate_dict
            )
        )
        for json_line in json_str.splitlines():
            out_stream.write("  {}\n".format(json_line))
    out_stream.write("]\n")


def assert_invalid_field_list(field_list):
    """raise d1_common.types.exceptions.InvalidRequest() if ``field_list`` contains any
    invalid field names. A list of the invalid fields is included in the exception.
    - Implicitly called by ``extract_values()``.

    """
    if field_list is not None:
        invalid_field_list = [
            v for v in field_list if v not in get_valid_field_name_list()
        ]
        if invalid_field_list:
            raise d1_common.types.exceptions.InvalidRequest(
                0, "Invalid fields: {}".format(", ".join(invalid_field_list))
            )


def get_valid_field_name_list():
    """Get a sorted list of valid field names."""
    return sorted(FIELD_NAME_TO_EXTRACT_DICT.keys())


# Private


def _create_query(filter_arg_dict, generate_dict):
    query = d1_gmn.app.models.ScienceObject.objects.filter(**(filter_arg_dict or {}))
    query = query.order_by("modified_timestamp", "id")
    # query = query.order_by("pid__did")
    query, annotate_key_list = _annotate_query(query, generate_dict)
    return query, annotate_key_list


def _annotate_query(query, generate_dict):
    """Add annotations to the query to retrieve values required by field value generate
    functions."""
    annotate_key_list = []
    for field_name, annotate_dict in generate_dict.items():
        for annotate_name, annotate_func in annotate_dict["annotate_dict"].items():
            query = annotate_func(query)
            annotate_key_list.append(annotate_name)
    return query, annotate_key_list


def _value_list_to_sciobj_dict(
    sciobj_value_list, lookup_list, lookup_dict, generate_dict
):
    """Create a dict where the keys are the requested field names, from the values
    returned by Django."""

    sciobj_dict = {}

    # for sciobj_value, lookup_str in zip(sciobj_value_list, lookup_list):
    lookup_to_value_dict = {k: v for k, v in zip(lookup_list, sciobj_value_list)}

    for field_name, r_dict in lookup_dict.items():
        if r_dict["lookup_str"] in lookup_to_value_dict.keys():
            sciobj_dict[field_name] = lookup_to_value_dict[r_dict["lookup_str"]]

    for field_name, annotate_dict in generate_dict.items():
        for final_name, generate_func in annotate_dict["generate_dict"].items():
            sciobj_dict[field_name] = generate_func(lookup_to_value_dict)

    return sciobj_dict


def _split_field_list(field_list):
    """Split the list of fields for which to extract values into lists by extraction
    methods.
    - Remove any duplicated field names.
    - Raises ValueError with list of any invalid field names in ``field_list``.

    """
    lookup_dict = {}
    generate_dict = {}

    for field_name in field_list or FIELD_NAME_TO_EXTRACT_DICT.keys():
        try:
            extract_dict = FIELD_NAME_TO_EXTRACT_DICT[field_name]
        except KeyError:
            assert_invalid_field_list(field_list)
        else:
            if "lookup_str" in extract_dict:
                lookup_dict[field_name] = extract_dict
            else:
                generate_dict[field_name] = extract_dict

    return lookup_dict, generate_dict


# Permission field


def _permission_annotate_subject(query):
    return query.annotate(
        permission_subject=django.contrib.postgres.aggregates.ArrayAgg(
            "permission__subject__subject"
        )
    )


def _permission_annotate_level(query):
    return query.annotate(
        permission_level=django.contrib.postgres.aggregates.ArrayAgg(
            "permission__level"
        )
    )


def _permission_extract(sciobj_dict):
    """Return a dict of subject to list of permissions on object."""
    return {
        perm_subj: ["read", "write", "changePermission"][: perm_level + 1]
        for perm_subj, perm_level in zip(
            sciobj_dict["permission_subject"], sciobj_dict["permission_level"]
        )
    }


"""Map field name to dict of information on how to extract that field
- ``extract_dict``: A dict with information about how to create the value for a given
  field.
- ``lookup_dict``: An ``extract_dict`` that selects single values using lookup strings.
- ``generate_dict``: An ``extract_dict``` that creates a complex value for a field with a
  combination of query annotation and one or more value generate functions.
"""
FIELD_NAME_TO_EXTRACT_DICT = {
    "pid": {"lookup_str": "pid__did"},
    "sid": {"lookup_str": "pid__chainmember_pid__chain__sid__did"},
    "obsoletes": {"lookup_str": "obsoletes__did"},
    "obsoletedby": {"lookup_str": "obsoleted_by__did"},
    "size": {"lookup_str": "size"},
    "checksum": {"lookup_str": "checksum"},
    "checksumalgorithm": {"lookup_str": "checksum_algorithm__checksum_algorithm"},
    "serialversion": {"lookup_str": "serial_version"},
    "formatid": {"lookup_str": "format__format"},
    "submitter": {"lookup_str": "submitter__subject"},
    "rightsholder": {"lookup_str": "rights_holder__subject"},
    "archived": {"lookup_str": "is_archived"},
    "dateuploaded": {"lookup_str": "uploaded_timestamp"},
    "datesysmetadatamodified": {"lookup_str": "modified_timestamp"},
    "originmembernode": {"lookup_str": "origin_member_node__urn"},
    "authoritativemembernode": {"lookup_str": "authoritative_member_node__urn"},
    "mediatype": {"lookup_str": "mediatype__name"},
    "filename": {"lookup_str": "filename"},
    "permissions": {
        "annotate_dict": {
            "permission_subject": _permission_annotate_subject,
            "permission_level": _permission_annotate_level,
        },
        "generate_dict": {"permission": _permission_extract},
    },
}
