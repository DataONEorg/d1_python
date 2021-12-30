#!/usr/bin/env python

import os
import re
import shutil

# import pip._internal.utils.misc
import importlib.metadata
import d1_dev.util
import pkg_resources


REQUIREMENTS_FILENAME = "requirements.txt"


# Modules in my dev environment that are not required by the stack

PACKAGE_EXCLUDE_REGEX_LIST = {
    "dataone.*",
    "ete3",
    "Flask",
    "logging-tree",
    "PyQt.*",
    "pyqt5",
    "python-magic",
    "redbaron",
}


def main():
    repo_dir = d1_dev.util.find_repo_root()
    req_path = os.path.join(repo_dir, REQUIREMENTS_FILENAME)
    req_backup_path = req_path + ".bak"
    try:
        os.remove(req_backup_path)
    except FileNotFoundError:
        pass
    shutil.move(req_path, req_backup_path)
    req_list = sorted(get_reqs())
    write_reqs(req_path, req_list)


def get_reqs():
    req_list = []
    for package_dist in pkg_resources.working_set:
        package_name = str(package_dist).split(' ')[0]
        if not is_filtered_package(package_name):
            req_str = str(package_dist.as_requirement())
            req_list.append(req_str)
    return req_list


def is_filtered_package(package_name):
    for filter_rx in PACKAGE_EXCLUDE_REGEX_LIST:
        if re.match(filter_rx, package_name, re.IGNORECASE):
            print("Filtered: {}".format(package_name, filter_rx))
            return True
    print("Included: {}".format(package_name))
    return False


def write_reqs(req_path, req_list):
    """Args:

    req_path: req_list:

    """
    with open(req_path, "w") as f:
        f.write("\n".join(req_list) + "\n")


if __name__ == "__main__":
    main()
