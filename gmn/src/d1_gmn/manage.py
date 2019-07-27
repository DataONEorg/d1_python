#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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

import os
import pkgutil
import sys

import django.core.management

# When running management commands, spurious DEBUG level log messages are written by
# some of the libraries that get loaded as dependencies for GMN. This disables DEBUG
# level logging altogether until we specifically enable it when needed.
# logging.disable(logging.DEBUG)

# An itsy bit of monkey patching to enable dashes in Django management commands without
# having to actually use dashes in the module names. Touching Django internals here,
# but catching exceptions. If internals change, The worse that should happen if this stops working is
# that the command names revert back to their names using underscores.
def find_commands(management_dir):
    command_dir = os.path.join(management_dir, "commands")
    return [
        name.replace("-", "")
        for _, name, is_pkg in pkgutil.iter_modules([command_dir])
        if not is_pkg and not name.startswith("_")
    ]


# django.core.management.find_commands = find_commands


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d1_gmn.settings")
    from django.core.management import execute_from_command_line

    # sys.argv[1].replace('-', '_')

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
