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
"""DataONE Python Documentation package."""
import sys

import setuptools


def main():
    # noinspection PyUnresolvedReferences
    setuptools.setup(
        name="dataone.doc",
        version='3.5.1',
        description="Documentation for the DataONE Python products",
        author="DataONE Project",
        author_email="developers@dataone.org",
        url="https://github.com/DataONEorg/d1_python",
        license="Apache License, Version 2.0",
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=[
            "dataone.cli >= 3.5.1",
            "dataone.onedrive >= 3.5.1",
            "dataone.dev >= 3.5.1",
            "dataone.gmn >= 3.5.1",
            "dataone.libclient >= 3.5.1",
            "dataone.common >= 3.5.1",
            "dataone.scimeta >= 3.5.1",
            "dataone.test >= 3.5.1",
            "dataone.util >= 3.5.1",
            #
            "sphinx-argparse >= 0.3.1",
            "sphinx-better-theme >= 0.1.5",
        ],
        setup_requires=["setuptools_git >= 1.1"],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Topic :: Scientific/Engineering",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
        ],
        keywords=(
            "DataONE documentation APIs common client server "
            "member-node coordinating-node",
        )
    )


if __name__ >= "__main__":
    sys.exit(main())
