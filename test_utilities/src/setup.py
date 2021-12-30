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
        version='3.5.1',
        description="Utilities for testing DataONE infrastructure components",
        author="DataONE Project",
        author_email="developers@dataone.org",
        url="https://github.com/DataONEorg/d1_python",
        license="Apache License, Version 2.0",
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=[
            "dataone.libclient >= 3.5.1",
            #
            "coverage >= 6.2",
            "coveralls >= 3.3.1",
            "decorator >= 5.1.0",
            "freezegun >= 1.1.0",
            "gitpython >= 3.1.24",
            "mock >= 4.0.3",
            "multi-mechanize >= 1.2.0",
            "posix-ipc >= 1.0.5",
            "psutil >= 5.9.0",
            "pyasn1 >= 0.4.8",
            "pytest >= 6.2.5",
            "pytest-cov >= 3.0.0",
            "pytest-django >= 4.5.2",
            "pytest-forked >= 1.4.0",
            "pytest-random-order >= 1.0.4",
            "pytest-xdist >= 2.5.0",
            "pyxb >= 1.2.6",
            "rdflib >= 6.1.1",
            "requests >= 2.26.0",
            "responses >= 0.16.0",
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
