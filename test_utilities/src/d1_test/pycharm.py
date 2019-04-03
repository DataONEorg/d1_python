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

"""PyCharm support in the test framework.

This sets up the path to the PyCharm binary. It is required and used only if pytest is
started with the --pycharm switch. Otherwise it is ignored.

When active, the test framework will:

    - Automatically open files where errors occur and move the cursor to the line of
      the error - Show syntax highlighted diffs for scripts and data files using
      PyCharm's powerful diff viewer

"""
import logging
import os
import select
import subprocess
import sys
import time

import d1_dev.util

try:
    import Xlib
    import Xlib.display

    is_headless = False
except ImportError:
    is_headless = True


logger = logging.getLogger(__name__)

# Set this path to the binary that launches PyCharm. If an environment variable
# of the same name exists, it is used instead of this setting.
PYCHARM_BIN_PATH = os.path.expanduser("~/bin/JetBrains/pycharm.sh")


def open_and_set_cursor(src_path, src_line=1):
    """Attempt to open the file at ``src_path`` in the PyCharm IDE and move the cursor
    to line ``src_line``

    - ``src_path`` can be an absolute path, or a path relative to the root of the
      DataONE Git repository.

    """
    if is_headless:
        return
    if src_path == "<string>":
        logger.debug("Unable to find location of error")
        return
    # Handle LocalPath from pytest
    src_path = str(src_path)
    src_path = _get_abs_path(src_path)
    _call_pycharm("--line", src_line, src_path)


def diff(left_path, right_path):
    """Attempt to open a diff of the two files in the PyCharm Diff & Merge tool."""
    if is_headless:
        return
    _tag_empty_file(left_path)
    _tag_empty_file(right_path)
    _call_pycharm("diff", left_path, right_path)
    _wait_for_diff_to_close(left_path, right_path)


def _wait_for_diff_to_close(left_path, right_path):
    """Wait for the user to close the diff window."""
    # Wait for window to open.
    logging.info("Waiting for PyCharm diff window to close. Press Enter to skip...")
    # Wait for window to open
    sleep_interval_sec = 0.1
    wait_sec = 3
    for i in range(int(wait_sec / sleep_interval_sec)):
        if _diff_window_is_open(left_path, right_path):
            break
        time.sleep(sleep_interval_sec)
    # Wait for window to close or for something to register on stdin.
    while True:
        # if select.select([sys.stdin], [], [], 0)[0]:
        #     break
        if not _diff_window_is_open(left_path, right_path):
            break
        time.sleep(sleep_interval_sec)


def _diff_window_is_open(left_path, right_path):
    """Return True if PyCharm is currently showing a diff window for the given paths.

    The search iterates over all windows managed by X and examines the properties /
    atoms. The window must have "jetbrains" as part of one or more classes and have
    "{left_path} vs {right_path}" as part of its window name.

    """
    display = Xlib.display.Display()
    net_wm_name = display.intern_atom("_NET_WM_NAME")  # Modern, UTF-8
    wm_name = display.intern_atom("WM_NAME")  # Legacy
    title_str = "{} vs {}".format(
        os.path.split(left_path)[1], os.path.split(right_path)[1]
    )

    def find_diff_window(window):
        for w in window.query_tree().children:
            if find_diff_window(w):
                return True
            else:
                if any(["jetbrains" in c for c in w.get_wm_class() or []]):
                    if title_str in get_window_name(w) or '':
                        return True
        return False

    def get_window_name(window_id):
        """Return window title if one can be found or None."""
        for atom in (net_wm_name, wm_name):
            window_obj = display.create_resource_object("window", window_id)
            name_str = window_obj.get_full_property(atom, 0).value
            if isinstance(name_str, bytes):
                return name_str.decode("latin1", "replace")
            return name_str

    try:
        return find_diff_window(display.screen().root)
    except (
        Xlib.error.XError,
        Xlib.error.BadWindow,
        UnicodeDecodeError,
        AttributeError,
    ):
        return False


def _tag_empty_file(path):
    """If path is to empty file, write the text "<empty>" to the file.

    - This works around the issue that PyCharm PyCharm Diff & Merge errors out if one
      of the input files are empty. - Is probably less confusing when debugging

    """
    if not os.path.getsize(path):
        with open(path, "w") as f:
            f.write("<empty>")


def _get_abs_path(src_path):
    if not os.path.isabs(src_path):
        src_path = os.path.join(d1_dev.util.find_repo_root_by_path(__file__), src_path)
    return src_path


def _call_pycharm(*arg_list):
    arg_list = list(map(str, arg_list))
    arg_str = ", ".join(arg_list)
    pycharm_bin_path = os.environ.get("PYCHARM_BIN_PATH", PYCHARM_BIN_PATH)
    try:
        assert os.path.isfile(pycharm_bin_path), (
            "PyCharm IDE integration has been enabled but the path to the PyCharm "
            "binary is incorrect. Please set the correct path in {}, PYCHARM_BIN_PATH"
            "or set the PYCHARM_BIN_PATH environment variable. If PyCharm is not "
            "available, try starting again without the --pycharm "
            "switch.".format(__file__)
        )
        subprocess.call([PYCHARM_BIN_PATH] + arg_list)
    except subprocess.CalledProcessError as e:
        logging.warning(
            'PyCharm call failed. error="{}" args="{}"'.format(str(e), arg_str)
        )
    else:
        logging.debug('PyCharm call ok. args="{}"'.format(arg_str))
