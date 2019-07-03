#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2013 DataONE
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
"""DataONE Utilities and Examples package."""
import os
import sys

import setuptools


def main():
    setuptools.setup(
        name="dataone.util",
        version="3.4.4",
        description="DataONE Utilities and Examples",
        author="DataONE Project",
        author_email="developers@dataone.org",
        url="https://github.com/DataONEorg/d1_tools",
        license="Apache License, Version 2.0",
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=["dataone.common >= 3.4.4", "dataone.libclient >= 3.4.4"],
        setup_requires=["setuptools_git >= 1.1"],
        entry_points={"console_scripts": gen_console_scripts()},
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
        ],
        keywords="DataONE python",
    )


def gen_console_scripts():
    return [
        "d1-{} = d1_util.{}:main".format(
            n.replace('_', '-').replace('.py', ''),
            n.replace('.py', '')
        )
        for n in os.listdir('./d1_util/') if n.endswith('.py')
    ]



if __name__ == "__main__":
    sys.exit(main())
