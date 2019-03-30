#!/usr/bin/env python

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
"""Create and manipulate access control objects."""

import d1_cli.impl.exceptions
import d1_cli.impl.util


class AccessControl:
    def __init__(self):
        self.allow = {}

    def __str__(self):
        return self._pretty_format()

    def get_list(self):
        return [(k, self.allow[k]) for k in sorted(self.allow.keys())]

    def add_allowed_subject(self, subject, permission):
        if permission is None:
            permission = "read"
        self._assert_valid_permission(permission)
        self._confirm_special_subject_write(subject, permission)
        self._add_allowed_subject(subject, permission)

    def remove_allowed_subject(self, subject):
        try:
            del self.allow[subject]
        except KeyError:
            raise d1_cli.impl.exceptions.InvalidArguments(
                "Subject not in access control list: {}".format(subject)
            )

    def clear(self):
        self.allow.clear()

    # Private.

    def _get_valid_permissions(self):
        """List of permissions, in increasing order."""
        return "read", "write", "changePermission"

    def _add_allowed_subject(self, subject, permission):
        self.allow[subject] = permission

    def _pretty_format(self):
        permissions = {}
        for allow in self.get_list():
            try:
                permissions[allow[1]].append(allow[0])
            except KeyError:
                permissions[allow[1]] = [allow[0]]
        lines = []
        for perm, perm_list in sorted(list(permissions.items())):
            lines.append(
                "  {0: <30s}{1}".format(perm, '"' + '", "'.join(sorted(perm_list)))
                + '"'
            )
        if not len(lines):
            lines = ["  None"]
        return "access:\n" + "\n".join(lines)

    def _assert_valid_permission(self, permission):
        if permission not in self._get_valid_permissions():
            msg = "Invalid permission: {}. Must be one of: {}".format(
                permission, ", ".join(self._get_valid_permissions())
            )
            raise d1_cli.impl.exceptions.InvalidArguments(msg)

    def _confirm_special_subject_write(self, subject, permission):
        if (
            subject in ("public", "authenticatedUser", "verifiedUser")
            and permission != "read"
        ):
            if not d1_cli.impl.util.confirm(
                "It is not recommended to give {} access to {}. Continue?".format(
                    permission, subject
                )
            ):
                raise d1_cli.impl.exceptions.InvalidArguments("Cancelled")
