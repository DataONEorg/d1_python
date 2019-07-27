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

"""Generate the reST (.rst) file for the GMN Management Commands from
the docstrings and `--help` text for the commands.
"""
import importlib
import logging
import os
import pathlib
import pkgutil
import textwrap

import d1_common.utils.filesystem
import d1_common.utils.ulog

import django

COMMAND_PACKAGE_TUP = (
    ("d1_gmn.app.management.commands", "./doc/rst/d1_gmn/operation/commands_generated.rst"),
)

# Inject reST strings based on the switches returned by `--help` for a command.
INJECT_TUP = (
    ("!--force ", "This command can be run safely in a production environment."),
    (
        "--public",
        """
        The ``--public`` switch causes GMN to ignore any available certificates and
        connect as the public user. This is useful if the source MN has only public
        objects or if a certificate that would be accepted by the source MN is not
        available.
        """,
    ),
)

log = logging.getLogger(__name__)


def main():
    gen_all()


def gen_all():
    # Configure GMN so that the GMN management commands can be imported.
    os.environ["DJANGO_SETTINGS_MODULE"] = "d1_gmn.settings_test"
    django.setup(set_prefix=False)
    # Log setup must be done after django_setup().
    # django.setup() configures its own logging, which is not the one set up in
    # settings.py.
    d1_common.utils.ulog.setup(is_debug=True)

    # It's cleaner to specify paths going out from root than up from here.
    d1_python_root_path = d1_common.utils.filesystem.abs_path('../../..')
    os.chdir(d1_python_root_path)


    for package_dot_path, rel_rst_path in COMMAND_PACKAGE_TUP:
        # abs_rst_path = d1_common.utils.filesystem.abs_path(rel_rst_path)
        gen_commands_page(package_dot_path, rel_rst_path)


def gen_commands_page(package_dot_path, rst_path):
    log.info(f"Generating {rst_path} for {package_dot_path}")
    package_obj = importlib.import_module(package_dot_path)
    with pathlib.Path(rst_path).open("w") as rst_file:
        for filefinder_, module_name, is_pkg in pkgutil.iter_modules(
            package_obj.__path__
        ):
            if not is_pkg and not module_name.startswith("_"):
                _gen_command_section(
                    package_obj, module_name, lambda s: _write_rst(rst_file, s)
                )


def _gen_command_section(package_obj, module_name, write_rst):
    module_dot_path = f"{package_obj.__name__}.{module_name}"
    log.info(f"Generating section for {module_dot_path}")
    module_obj = importlib.import_module(module_dot_path)
    doc_str = module_obj.__doc__ or ""
    header_str = f"\n**{module_name}**"
    # write_rst(f'\n{module_name.replace("_", "-")}')
    write_rst(f"{header_str}")
    write_rst(f'{"-" * len(header_str)}')
    write_rst(f"\n{doc_str.strip()}")
    # write_rst(f"\n.. djcommand:: {module_dot_path}")
    parser = module_obj.Command().create_parser(module_name, "")
    help_str = parser.format_help().split("optional arguments:")[1]
    # print(help_str)
    _inject(write_rst, help_str)
    write_rst(f"\n.. highlight:: none")
    write_rst(f"\n::")
    write_rst(f"{textwrap.indent(help_str, ' ' * 4)}")


def _write_rst(rst_file, s):
    # print(s)
    rst_file.write(f"{s}\n")


def _inject(write_rst, help_str):
    for match_str, inject_str in INJECT_TUP:
        is_negated = match_str.startswith("!")
        if is_negated ^ (match_str.lstrip("!") in help_str):
            write_rst(f"\n{textwrap.dedent(inject_str)}")


if __name__ == "__main__":
    main()
