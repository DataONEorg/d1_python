#!/usr/bin/env python

import shutil
import d1_dev.util
import os
import pip._internal.utils.misc
import re


REQUIREMENTS_FILENAME = 'requirements.txt'


# Modules in my dev environment that are not required by the stack

MODULE_FILTER_REGEX_LIST = {
    'beautifulsoup',
    'black',
    'bs4',
    'dataone.*',
    'ete3',
    'Flask',
    'logging-tree',
    'PyQt.*',
    'pyqt5',
    'python-magic',
    'redbaron',
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
    # noinspection PyProtectedMember
    for package_dist in pip._internal.utils.misc.get_installed_distributions(local_only=True):
        if not is_filtered_package(package_dist.project_name):
            req_str = str(package_dist.as_requirement())
            req_list.append(req_str)
    return req_list

def is_filtered_package(project_name):
    for filter_rx in MODULE_FILTER_REGEX_LIST:
        if re.match(filter_rx, project_name, re.IGNORECASE):
            print('Filtered: {}'.format(project_name, filter_rx))
            return True
    print('Included: {}'.format(project_name))
    return False


def write_reqs(req_path, req_list):
    """
    Args:
        req_path:
        req_list:
    """
    with open(req_path, 'w') as f:
        f.write('\n'.join(req_list) + "\n")


if __name__ == '__main__':
    main()
