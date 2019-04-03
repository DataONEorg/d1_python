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

"""Utilities for filesystem paths and operations."""

import os
import sys
import urllib.parse

FILENAME_SAFE_CHARS = ' @$,~*&'


def gen_safe_path(*path_list):
    """Escape characters that are not allowed or often cause issues when used in file-
    or directory names, then join the arguments to a filesystem path.

    Args:
        positional args: str
            Strings to use as elements in a filesystem path, such as PID, SID or URL.

    Returns:
        str : A path safe for use as a as a file- or directory name.

    """
    return os.path.join(*[gen_safe_path_element(p) for p in path_list])


def gen_safe_path_element(s):
    """Escape characters that are not allowed or often cause issues when used in file-
    or directory names.

    Args:
        s: str
            Any string, such as a PID, SID or URL

    Returns:
        str : A string safe for use as a file- or directory name.

    """
    return urllib.parse.quote(s.encode('utf-8'), safe=FILENAME_SAFE_CHARS)


def create_missing_directories_for_file(file_path):
    """Create any directories in ``dir_path`` that do not yet exist.

    Args:
      file_path : str
        Relative or absolute path to a file that may or may not exist.

        Must be a file path, as any directory element at the end of the path will not
        be created.

    See Also:
      create_missing_directories_for_dir()

    """
    create_missing_directories_for_dir(os.path.dirname(file_path))


def create_missing_directories_for_dir(dir_path):
    """Create any directories in ``dir_path`` that do not yet exist.

    Args:
      dir_path : str
        Relative or absolute path to a directory that may or may not exist.

        Must be a directory path, as any filename element at the end of the path will also
        be created as a directory.

    See Also:
      create_missing_directories_for_file()

    """
    os.makedirs(dir_path, exist_ok=True)


def abs_path_from_base(base_path, rel_path):
    """Join a base and a relative path and return an absolute path to the resulting
    location.

    Args:
      base_path: str
        Relative or absolute path to prepend to ``rel_path``.

      rel_path: str
        Path relative to the location of the module file from which this function is called.

    Returns:
        str : Absolute path to the location specified by ``rel_path``.

    """
    # noinspection PyProtectedMember
    return os.path.abspath(
        os.path.join(
            os.path.dirname(sys._getframe(1).f_code.co_filename), base_path, rel_path
        )
    )


def abs_path(rel_path):
    """Convert a path that is relative to the module from which this function is called,
    to an absolute path.

    Args:
      rel_path: str
        Path relative to the location of the module file from which this function is called.

    Returns:
        str : Absolute path to the location specified by ``rel_path``.

    """
    # noinspection PyProtectedMember
    return os.path.abspath(
        os.path.join(os.path.dirname(sys._getframe(1).f_code.co_filename), rel_path)
    )
