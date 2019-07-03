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
"""Generator that resolves a list of file and dir paths and returns file paths with
optional filtering and client feedback."""
import argparse
import fnmatch
import logging
import os

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


DEFAULT_EXCLUDE_GLOB_LIST = [
    # Dirs
    "*egg-info/",
    ".git/",
    ".idea/",
    "__pycache__/",
    ".eggs/",
    ".pytest_cache/",
    "build/",
    "dist/",
    "doc/",
    "generated/",
    "migrations/",
    # Files
    "*~",
    "*.bak",
    "*.tmp",
    "*.pyc",
]


def path_generator(
    path_list,
    include_glob_list=None,
    exclude_glob_list=None,
    recursive=True,
    ignore_invalid=False,
    default_excludes=True,
    return_entered_dir_paths=False,
    return_skipped_dir_paths=False,
):
    """# language=rst.

    Args:
      path_list: list of str

        List of file- and dir paths. File paths are used directly and dirs are searched
        for files.

        ``path_list`` does not accept glob patterns, as it's more convenient to let the
        shell expand glob patterns to directly specified files and dirs. E.g., to use a
        glob to select all .py files in a subdir, the command may be called with
        sub/dir/*.py, which the shell expands to a list of files, which are then passed
        to this function. The paths should be Unicode or utf-8 strings. Tilde ("~") to
        home expansion is performed on the paths.

        The shell can also expand glob patterns to dir paths or a mix of file and dir
        paths.

      include_glob_list: list of str
      exclude_glob_list: list of str

        Patterns ending with "/" are matched only against dir names. All other patterns
        are matched only against file names.

        If the include list contains any file patterns, files must match one or more of
        the patterns in order to be returned.

        If the include list contains any dir patterns, dirs must match one or more of
        the patterns in order for the recursive search to descend into them.

        The exclude list works in the same way except that matching files and dirs are
        excluded instead of included. If both include and exclude lists are specified,
        files and dirs must both match the include and not match the exclude patterns in
        order to be returned or descended into.

      recursive: bool

        - **True** (default): Search subdirectories
        - **False**: Do not search subdirectories

      ignore_invalid: bool

        - **True**: Invalid paths in path_list are ignored.
        - **False** (default): EnvironmentError is raised if any of the paths in
          ``path_list`` do not reference an existing file or dir.

      default_excludes: bool

        - **True**: A list of glob patterns for files and dirs that should typically be
          ignored is added to any exclude patterns passed to the function. These
          include dirs such as .git and backup files, such as files appended with "~".
        - **False**: No files or dirs are excluded by default.

      return_entered_dir_paths: bool

        - **False**: Only file paths are returned.
        - **True**: Directory paths are also returned.

      return_skipped_dir_paths: bool

        - **False**: Paths of skipped dirs are not returned.
        - **True**: Paths of skipped dirs are returned.

        The iterator never descends into excluded dirs, and by default, does not return
        the paths of excluded dirs. However, the client may need to get the paths of
        dirs that were excluded instead of dirs that were included. E.g., when looking
        for dirs to delete.

    Returns:
      File path iterator

    Notes:

      During iteration, the iterator can be prevented from descending into a directory
      by sending a "skip" flag when the iterator yields the directory path. This allows
      the client to determine if directories should be iterated by, for instance, which
      files are present in the directory. This can be used in conjunction with the
      include and exclude glob lists. Note that, in order to receive directory paths
      that can be skipped, ``return_entered_dir_paths`` must be set to True.

      The regular ``for...in`` syntax does not support sending the "skip" flag back to
      the iterator. Instead, use a pattern like:

      .. highlight: python

      ::

        itr = file_iterator.file_iter(..., return_entered_dir_paths=True)
        try:
          path = itr.next()
          while True:
          skip_dir = determine_if_dir_should_be_skipped(path)
          file_path = itr.send(skip_dir)
        except KeyboardInterrupt:
          raise StopIteration
        except StopIteration:
          pass

      Glob patterns are matched only against file and directory names, not the full
      paths.

      Paths passed directly in ``path_list`` are not filtered.

      The same file can be returned multiple times if ``path_list`` contains duplicated
      file paths or dir paths, or dir paths that implicitly include the same subdirs.

      ``include_glob_list`` and ``exclude_glob_list`` are handy for filtering the files
      found in dir searches.

      Remember to escape the include and exclude glob patterns on the command line so
      that they're not expanded by the shell.

    """
    include_glob_list = include_glob_list or []
    exclude_glob_list = exclude_glob_list or []

    if default_excludes:
        exclude_glob_list += DEFAULT_EXCLUDE_GLOB_LIST

    log.debug("file_iter():")
    log.debug(f"  paths: {', '.join(path_list)}")
    log.debug(f"  include: {', '.join(include_glob_list)}")
    log.debug(f"  exclude: {', '.join(exclude_glob_list)}")
    log.debug(f"  recursive: {recursive}")
    log.debug(f"  ignore_invalid: {ignore_invalid}")
    log.debug(f"  default_excludes: {default_excludes}")
    log.debug(f"  return_entered_dir_paths: {return_entered_dir_paths}")
    log.debug(f"  return_skipped_dir_paths: {return_skipped_dir_paths}")
    log.debug("")

    include_file_glob_list = [
        p for p in include_glob_list if not p.endswith(os.path.sep)
    ]
    exclude_file_glob_list = [
        p for p in exclude_glob_list if not p.endswith(os.path.sep)
    ]
    include_dir_glob_list = [p for p in include_glob_list if p.endswith(os.path.sep)]
    exclude_dir_glob_list = [p for p in exclude_glob_list if p.endswith(os.path.sep)]

    for path in path_list:
        path = os.path.expanduser(path)

        # Return file
        if os.path.isfile(path):
            file_name = os.path.split(path)[1]
            if not _is_filtered(
                file_name, include_file_glob_list, exclude_file_glob_list
            ):
                yield path

        # Search directory
        elif os.path.isdir(path):
            yield from _filtered_walk(
                path,
                include_dir_glob_list,
                exclude_dir_glob_list,
                include_file_glob_list,
                exclude_file_glob_list,
                return_entered_dir_paths,
                return_skipped_dir_paths,
                recursive,
            )

        else:
            if not ignore_invalid:
                raise EnvironmentError(0, "Not a valid file or dir path", path)


def _filtered_walk(
    root_dir_path,
    include_dir_glob_list,
    exclude_dir_glob_list,
    include_file_glob_list,
    exclude_file_glob_list,
    return_entered_dir_paths,
    return_skipped_dir_paths,
    recursive,
):
    skip_dir_path_list = []

    for dir_path, dir_list, file_list in os.walk(root_dir_path):
        if not recursive and dir_path != root_dir_path:
            return

        if any(dir_path.startswith(d) for d in skip_dir_path_list):
            log.debug(f"Skipped dir branch: {dir_path}")
            continue

        enter_dir_list = []
        for dir_name in dir_list:
            if not _is_filtered(
                os.path.split(dir_name)[1] + "/",
                include_dir_glob_list,
                exclude_dir_glob_list,
            ):
                enter_dir_list.append(dir_name)
            else:
                if return_skipped_dir_paths:
                    yield os.path.join(dir_path, dir_name)

        dir_list[:] = enter_dir_list

        if return_entered_dir_paths:
            for dir_name in dir_list:
                this_dir_path = os.path.join(dir_path, dir_name)
                skip_dir = yield this_dir_path
                if skip_dir:
                    log.debug(f"Client requested skip of branch: {this_dir_path}")
                    skip_dir_path_list.append(this_dir_path)

        for file_name in file_list:
            if not _is_filtered(
                file_name, include_file_glob_list, exclude_file_glob_list
            ):
                yield os.path.join(dir_path, file_name)


def _is_filtered(name, include_glob_list, exclude_glob_list):
    return (
        include_glob_list
        and not any(fnmatch.fnmatch(name, g) for g in include_glob_list)
        or exclude_glob_list
        and any(fnmatch.fnmatch(name, g) for g in exclude_glob_list)
    )


# =====================================================================================


class ArgParser:
    """An argparse.ArgumentParser populated with a standard set of command line
    arguments for controlling the path generator from the command line.

    The script that calls this function will typically add its own specific arguments by
    making additional ``parser.add_argument()`` calls.

    When creating the path_generator, simply pass ``parser.path_arg_dict`` to
    `path_generator()`.

    Example:
        import d1_common.iter.path

        parser = d1_common.iter.path.ArgParser(
            __doc__,
            # Set non-configurable values
            include_glob_list=['*.py'],
            return_entered_dir_paths=True,
        )
        # Add command specific arguments
        parser.add_argument(...)
        # Create the path_generator and iterate over the resulting paths
        for p in d1_common.iter.path.path_generator(parser.path_arg_dict):
            print(p)
    """

    # From Python 3.7, dicts keep their insertion order, so no list of keys in preferred
    # order is needed.
    ARG_DICT = {
        "path_list": ("path", dict(nargs="+", help="File or directory path")),
        "exclude_glob_list": (
            "--exclude",
            dict(
                default=DEFAULT_EXCLUDE_GLOB_LIST,
                nargs="+",
                metavar="glob",
                help="Exclude glob patterns",
            ),
        ),
        "include_glob_list": (
            "--include",
            dict(nargs="+", metavar="glob", help="Exclude glob patterns"),
        ),
        "recursive": (
            "--no-recursive",
            dict(action="store_false", help="Do not search directories recursively"),
        ),
        "ignore_invalid": (
            "--ignore-invalid",
            dict(action="store_true", help="Ignore invalid paths"),
        ),
        "default_excludes": (
            "--no-default-excludes",
            dict(action="store_false", help="Don't add default glob exclude patterns"),
        ),
        "return_entered_dir_paths": (
            "--return-entered-dir-paths",
            dict(
                action="store_true",
                help="Return the paths of dirs that the generator enters",
            ),
        ),
        "return_skipped_dir_paths": (
            "--return-skipped-dir-paths",
            dict(
                action="store_true",
                help="Return the paths of dirs that the generator enters",
            ),
        ),
    }

    def __init__(
        self,
        description_str=None,
        # formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        **val_dict,
    ):
        """Create a ArgumentParser populated with a standard set of command line
        arguments for controlling the path generator from the command line.

        Args:
            description_str: Description of the command
                The description is included in the automatically generated help message.

            formatter_class:
                Modify the help message format. See the `argparse` module for available
                Formatter classes.

            fixed value overrides:
                Passing any of these arguments causes provided value to be used when
                instantiating the path generator, and the corresponding command line
                argument to become hidden and unavailable.

                fixed_path_list
                fixed_exclude_glob_list
                fixed_include_glob_list
                fixed_recursive
                fixed_ignore_invalid
                fixed_default_excludes
                fixed_return_entered_dir_paths
                fixed_return_skipped_dir_paths

            default value overrides:
                Passing any of these arguments causes the provided value to be used
                as the default. The corresponding command line argument is still
                available and can be used to override the default value

                default_path_list
                default_exclude_glob_list
                default_include_glob_list
                default_recursive
                default_ignore_invalid
                default_default_excludes
                default_return_entered_dir_paths
                default_return_skipped_dir_paths
        """
        self._assert_valid_val_dict(val_dict)
        self._val_dict = val_dict
        self._parser = argparse.ArgumentParser(
            description=description_str, formatter_class=formatter_class
        )
        self._add_parser_arguments()
        self._args = None
        self._path_arg_dict = None

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

    @property
    def path_arg_dict(self):
        """Get command line arguments as dict suitable for passing to a
        path_generator create call via argument unpacking.

        Returns:
            dict: Arguments valid for passing to path_generator() create call.

            The dict will include any fixed value substitutions that were passed to
            __init__() via the val_dict.
        """
        if self._path_arg_dict is None:
            args_dict = vars(self._args)
            self._path_arg_dict = {}
            for k in ArgParser.ARG_DICT.keys():
                if f"fixed_{k}" in self._val_dict:
                    v = self._val_dict[f"fixed_{k}"]
                else:
                    v = args_dict["path" if k == "path_list" else k]
                self._path_arg_dict[k] = v
        return self._path_arg_dict

    def _assert_valid_val_dict(self, val_dict):
        for k in val_dict:
            assert k.startswith("fixed_") or k.startswith(
                "default_"
            ), "Value overrides must start with 'fixed_' or 'default_'"
            assert (
                k.replace("fixed_", "").replace("default_", "")
                in ArgParser.ARG_DICT.keys()
            ), "Value overrides must correspond to path_generator() arguments"

    def _add_parser_arguments(self):
        group = self._parser.add_argument_group("Paths")

        for arg_key in ArgParser.ARG_DICT.keys():
            arg_name, param_dict = ArgParser.ARG_DICT[arg_key]
            # Do not add parser arguments for values where a fixed override has been
            # provided.
            if f"fixed_{arg_key}" in self._val_dict:
                continue
            # Modify the default if a default override has been provided.
            if f"default_{arg_key}" in self._val_dict:
                param_dict["default"] = self._val_dict[f"default_{arg_key}"]
            # Work around that dest cannot be specified for positional args in
            # argparse.
            if arg_key != "path_list":
                param_dict["dest"] = arg_key
            group.add_argument(arg_name, **param_dict)

        self._parser.add_argument_group("Command")
        self._parser.add_argument(
            "--debug", action="store_true", help="Debug level logging"
        )
