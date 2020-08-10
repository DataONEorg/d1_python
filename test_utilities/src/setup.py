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
"""DataONE Test Utilities package."""
import sys

import setuptools


def main():
    setuptools.setup(
        name="dataone.test_utilities",
        version='3.5.0',
        description="Utilities for testing DataONE infrastructure components",
        author="DataONE Project",
        author_email="developers@dataone.org",
        url="https://github.com/DataONEorg/d1_python",
        license="Apache License, Version 2.0",
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=[
            "dataone.libclient >= 3.5.0",
            #
            "coverage >= 5.2.1",
            "coveralls >= 2.1.1",
            "decorator >= 4.4.2",
            "freezegun >= 0.3.15",
            "gitpython >= 3.1.7",
            "mock >= 4.0.2",
            "multi-mechanize >= 1.2.0",
            "posix-ipc >= 1.0.4",
            "psutil >= 5.7.2",
            "pyasn1 >= 0.4.8",
            "pytest >= 6.0.1",
            "pytest-cov >= 2.10.0",
            "pytest-django >= 3.9.0",
            "pytest-forked >= 1.3.0",
            "pytest-random-order >= 1.0.4",
            "pytest-xdist >= 1.34.0",
            "pyxb >= 1.2.6",
            "rdflib >= 5.0.0",
            "requests >= 2.24.0",
            "responses >= 0.10.15",
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
            "DataONE source code unit tests ingeration tests coverage travis "
            "coveralls"
        ),
    )


if __name__ == "__main__":
    sys.exit(main())
