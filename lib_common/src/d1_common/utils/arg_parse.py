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
import argparse
import logging


# noinspection PyUnresolvedReferences
class ArgParserBase(object):
    def __init__(self, description_str=None, argument_parser=None, **val_dict):
        self._val_dict = val_dict
        self._assert_valid_val_dict()
        self._log = logging.getLogger(__name__)
        if argument_parser is None:
            self._parser = argparse.ArgumentParser(
                description=description_str,
                formatter_class=argparse.RawDescriptionHelpFormatter,
            )
        else:
            self._parser = argument_parser

        self._add_parser_arguments()
        self._args = None
        self._get_method_args = None

    def add_argument(self, *arg_list, **arg_dict):
        """Add command specific arguments."""
        self._parser.add_argument(*arg_list, **arg_dict)

    @property
    def args(self):
        """Get complete command line arguments as Namespace object.

        Returns:
            Namespace: Complete command line arguments.

            This is an exact representation of the parsed command line and does not
            include any fixed value substitutions from the val_dict passed to
            __init__().
        """
        if self._args is None:
            self._args = self._parser.parse_args()
        return self._args

    def get_method_args(self, opt_dict=None):
        """Get command line arguments as dict suitable for passing to a path_generator
        create call via argument unpacking.

        Returns:
            dict: Arguments valid for passing to the object being created.

            The dict will include any fixed value substitutions that were passed to
            __init__() via the val_dict.
        """
        if self._get_method_args is None:
            args_dict = opt_dict or vars(self.args)
            self._get_method_args = {}
            for k, v in self.parser_dict.items():
                if f"fixed_{k}" in self._val_dict:
                    v = self._val_dict[f"fixed_{k}"]
                else:
                    # v = args_dict["path" if k == "path_list" else k]
                    try:
                        v = args_dict[k]
                    except KeyError:
                        raise ValueError("{} {}".format(k, ", ".join(args_dict)))
                self._get_method_args[k] = v
        self._dump_arg_dict(self._get_method_args)
        return self._get_method_args

    def _dump_arg_dict(self, arg_dict):
        for k, v in arg_dict.items():
            self._log.error("{} {}: {}".format(__file__, k, v))

    def _assert_valid_val_dict(self):
        for k in self._val_dict:
            if not (k.startswith("fixed_") or k.startswith("default_")):
                raise ValueError(
                    "Argument names for value overrides must start with "
                    '"fixed_" or "default_". arg="{}"'.format(k)
                )

            orig_arg_name = k.replace("fixed_", "").replace("default_", "")

            if orig_arg_name not in self.parser_dict.keys():
                raise ValueError(
                    "Argument name for value override must correspond with "
                    'keys in arg_dict. arg="{}" arg_dict_keys="{}"'.format(
                        orig_arg_name, ", ".join(self.parser_dict.keys())
                    )
                )

    def _add_parser_arguments(self):
        common = self._parser.add_argument_group("Common")
        try:
            common.add_argument(
                "--debug", action="store_true", help="Debug level logging"
            )
        except argparse.ArgumentError:
            pass

        group = self._parser.add_argument_group(self.parser_name)
        for arg_key in self.parser_dict.keys():
            arg_name, param_dict = self.parser_dict[arg_key]
            # Do not add parser arguments for values where a fixed override has been
            # provided.
            if f"fixed_{arg_key}" in self._val_dict:
                continue
            # Modify the default if a default override has been provided.
            if f"default_{arg_key}" in self._val_dict:
                param_dict["default"] = self._val_dict[f"default_{arg_key}"]
            try:
                if arg_name.startswith("-"):
                    # self._log.debug(
                    #     f'add_argument() "{arg_name}" '
                    #     f'dest="{arg_key}" param_dict="{param_dict}"'
                    # )
                    group.add_argument(arg_name, dest=arg_key, **param_dict)
                else:
                    # self._log.debug(
                    #     f'add_argument() "{arg_key}" '
                    #     f'metavar="{arg_name}" param_dict="{param_dict}"'
                    # )
                    group.add_argument(arg_key, metavar=arg_name, **param_dict)

            except ValueError as e:
                self._log.error(
                    'Unable to add arg. arg_name="{}" param_dict="{}" error="{}" '.format(
                        arg_name, param_dict, str(e)
                    )
                )
