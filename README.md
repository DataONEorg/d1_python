
## d1_python

Python components for DataONE clients and servers.

See the [documentation on ReadTheDocs](http://dataone-python.readthedocs.io/en/latest/).

[![Build Status](https://travis-ci.org/DataONEorg/d1_python.svg?branch=master)](https://travis-ci.org/DataONEorg/d1_python)
[![Coverage Status](https://coveralls.io/repos/github/DataONEorg/d1_python/badge.svg?branch=master)](https://coveralls.io/github/DataONEorg/d1_python?branch=master)
[![Documentation Status](https://readthedocs.org/projects/dataone-python/badge/?version=latest)](http://dataone-python.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/dataone.common.svg)](https://badge.fury.io/py/dataone.common)

### v2 and v1 API

* DataONE Generic Member Node:
[PyPI](https://pypi.python.org/pypi/dataone.gmn) &ndash;
[Docs](http://dataone-python.readthedocs.io/en/latest/gmn/index.html)
* DataONE Client Library for Python:
[PyPI](https://pypi.python.org/pypi/dataone.libclient) &ndash;
[Docs](http://dataone-python.readthedocs.io/en/latest/client/index.html)
* DataONE Common Library for Python: &ndash;
[PyPI](https://pypi.python.org/pypi/dataone.common) &ndash;
[Docs](http://dataone-python.readthedocs.io/en/latest/common/index.html)
* DataONE Test Utilities:
[PyPI](https://pypi.python.org/pypi/dataone.test_utilities) &ndash;
[Docs](http://dataone-python.readthedocs.io/en/latest/test/index.html)

### v1 API

* DataONE Command Line Client (CLI):
[PyPI](https://pypi.python.org/pypi/dataone.cli) &ndash;
[Docs](http://dataone-python.readthedocs.io/en/latest/cli/index.html)
* DataONE ONEDrive:
[PyPI](https://pypi.python.org/pypi/dataone.onedrive) &ndash;
[Docs](http://dataone-python.readthedocs.io/en/latest/onedrive/index.html)
* DataONE Certificate Extensions:
[PyPI](https://pypi.python.org/pypi/dataone.certificate_extensions)
* DataONE Gazetteer:
[PyPI](https://pypi.python.org/pypi/dataone.gazetteer)
* DataONE Ticket Generator:
[PyPI](https://pypi.python.org/pypi/dataone.ticket_generator)
* Google Foresite Toolkit:
[PyPI](https://pypi.python.org/pypi/google.foresite-toolkit)

### Contributing

Pull Requests (PRs) are welcome! Before you start coding, feel free to reach out to us and let us know what you plan to implement. We might be able to point you in the right direction.

We try to follow [PEP8](https://www.python.org/dev/peps/pep-0008/), with the main exception being that we use two instead of four spaces per indent.

To help keep the style consistent and commit logs, blame/praise and other code annotations accurate, we use the following `pre-commit` hooks to automatically format and check Python scripts before committing to GitHub:

* [YAPF](https://github.com/google/yapf) - PEP8 formatting with DataONE modifications
* [isort](https://github.com/timothycrosley/isort) - Sort and group imports
* [trailing-whitespace](git://github.com/pre-commit/pre-commit-hooks) - Remove trailing whitespace
* [Flake8](http://flake8.pycqa.org/en/latest/) - Lint, code and style validation

Configuration files for YAPF (`./.flake8`), isort (`./.isort.cfg`) and Flake8
(`./.style.yapf`) are included, and show the formatting options we have
selected.

Contributors are encouraged to set up the hooks before creating PRs. This can be done automagically with [pre-commit](pre-commit.com), for which a configuration file is also included.

To set up automatic validation and formatting:

    $ sudo pip install pre-commit
    $ cd <a folder in the Git working tree for the repository>
    $ pre-commit autoupdate
    $ pre-commit install

Notes:

* If the `YAPF`, `isort` or `trailing-whitespace` hooks modify any of the files being committed, the hooks will show as `Failed` and the commit is aborted. This provides an opportunity to examine the reformatted files and run the unit and integration tests again in order make sure the reformat did not break anything. The modified files can then be staged and committed again. If no new modifications have been made, the commit then goes through, with the hooks showing a status of `Passed`.

  A convenient command to "restage" the files modified by pre-commit:

      $ git update-index --again

  Or, to add a shortcut:

      $ git config --global alias.restage "update-index --again"

      $ git restage


* `Flake8` only performs validation, not formatting. If validation fails, the issues should be fixed before committing. The modifications may then trigger a new formatting by `YAPF` and/or `trailing-whitespace`, thus requiring the files to be staged and commited again.

* If desired, the number of extra staging and commits caused by reformatting and validation can be reduced with workflow adjustments:

  * **trailing whitespace**: Use an editor that can strip trailing whitespace on save. E.g., for PyCharm, this setting is at `Editor > General > Strip trailing spaces on Save`.

  * **YAPF formatting**: Call `YAPF` manually on the file before commit. `YAPF` searches from current directory and up in the tree for configuration files. So, as long as current directory is in the repository root or below, `YAPF` should pick up and use the configuration that is included in the repository. To call `YAPF` manually, it can either be installed separately, or an alias can be set up to call the version that `pre-commit` has installed into its own venv.

  * **Flake8 validation**: the same procedure as for `YAPF` can be used, as `Flake8` searches for its configuration file in the same way. In addition, IDEs can typically do code inspections and tag issues directly in the UI, where they can be handled before commit.


### Unit tests

Testing is based on the [pytest](https://docs.pytest.org/en/latest/) unit test framework.

#### Sample files

Most of our tests work by serializing objects generated by the code being tested and comparing them with reference samples stored in files. This allows us to check all properties of generated objects without having to write asserts that check individual properties, eliminating a time consuming and repetitive part of the test writing process.

When writing comparisons manually, one will often select a few properties to check, and when those are determined to be valid, the remaining values are assumed to be correct as well. By comparing complete serialized versions of the objects, we avoid such assumptions.

By storing the expected serialized objects in files instead of in the unit tests themselves, we avoid embedding hard coded documents inside the unit test modules and make it simple to automatically update the expected contents of objects as the code evolves.

When unit tests are being run as part of CI or as a normal guard against regressions in a local development environment, any mismatches between actual and expected serialized versions of objects simply trigger test failures. However, when a test is initially created or the serialized version of an object is expected to change, tests can automatically write or update the sample files they use. This function is enabled by starting `pytest` with the `--sample-ask` switch. When enabled, missing or mismatched sample files will not trigger test failures, instead starting an interactive process where differences are displayed together with yes/no prompts for writing or updating the samples. By default, differences are displayed in a GUI window using `kdiff3`, which provides a nice color coded view of the differences.

The normal procedure for writing a sample based unit test is to just write the test as if the sample already exists, then running the test with `--sample-ask` and viewing and approving the resulting sample, which is then automatically written to a file. The sample file name is displayed, making it easy to find the file in order to add it to tracking so that it can be committed along with the test module.

When working on large changes that cause many samples to become outdated, reviewing and approving samples can be deferred until the new code approaches stability. This is done by running the tests with `--sample-write`, which automatically writes or updates samples to match the current results. Then, view and approve the tests with `--sample-review` before committing.  

Typically, it is not desirable to track generated files in Git. However, although the sample files are generated, they are an integral part of the units tests, and should be tracked just like the unit tests themselves.

Also implemented is a simple process for cleaning out unused sample files. Sample files are often orphaned when their corresponding tests are removed or refactored. The process is activated with the `--sample-tidy` switch. When active, the test session starts by moving all sample files from their default directory, `test_docs`, to `test_docs_tidy`. As the sample files are accessed by tests, they are automatically moved back to `test_docs`, and any files remaining in `test_docs_tidy` after a complete test run can be untracked and deleted.

When staging `test_docs`, stage the directory, so that new files are included, and deleted files get deleted on the server:

    $ git add test_utilities/src/d1_test/test_docs
    $ git commit -m 'Update samples'

#### DataONE Client to Django test adapter

GMN tests are based on an adapter that enables using d1_client with the Django test framework. The adapter mocks Requests to issue requests through the Django test client.

Django includes a test framework with a test client that provides an interface that's similar to that of an HTTP client, but calls Django internals directly. The client enables testing of most functionality of a Django app without actually starting the app as a network service.

For testing GMN's D1 REST interfaces, we want to issue the test requests via the D1 MN client. Without going through the D1 MN client, we would have to reimplement much of what the client does, related to formatting and parsing D1 REST requests and responses.

This module is typically used in tests running under django.test.TestCase and requires an active Django context, such as the one provided by `./manage.py test`.

#### Command line switches

We have added some custom functionality to pytest which can be enabled to launching pytest with the following switches:

  * `--sample-ask`: Enable a mode that invokes `kdiff3` to display diffs and, after user confirmation, can automatically update or write new test sample documents on mismatches.

  * `parameterize_dict`: Support for parameterizing test functions by adding a dict class member containing parameter sets.

  * `--pycharm`: Attempt to move the cursor in PyCharm to the location of the test of failure.

  * See `./conftest.py` for implementation and notes.

#### Debugging tests with PyCharm

* By default, the PyCharm `Run context configuration (Ctrl+Shift+F10)` will generate test configurations and run the tests under the native unittest framework in Python's standard library. This will cause the tests to fail as they require pytest. To generate pytest configurations by default, set `Settings > Tools > Python Integrated Tools > Default test runner` to py.test. See the [documentation](https://www.jetbrains.com/help/pycharm/2017.1/testing-frameworks.html) for details.

* Generate and run a configuration for a specific test by placing the cursor on a test function name and running `Run context configuration (Ctrl+Shift+F10)`.

* After generating the configuration, debug with `Debug (Shift-F9)`.

* If running the tests outside of PyCharm, launching `pytest` with the `--pycharm` switch will cause `pytest` to attempt to move the cursor in PyCharm to the location of any tests failures as they occur. This should be used with the `--exitfirst` (`-x`) switch.

* Stopping a test that has hit a breakpoint in PyCharm can cause the test database to be left around. On the next run, Django will then prompt the user to type "yes" to remove the database. The prompt appears in the PyCharm debug console output. To disable the prompt, go to `Run / Debug Configurations > Edit Configurations > Defaults > Django tests > Options` and add `--noinput`. See the [question on SO](https://stackoverflow.com/questions/34244171) for details.

* `pytest` by default captures `stdout` and `stderr` output for the tests and only shows the output for the tests that failed after all tests have been completed. Since a test that hits a breakpoint has not yet failed, this hides any output from tests being debugged and also hides output from the debug console prompt (where Python script can be evaluated in the current context). To see the output while debugging, go to `Run / Debug Configurations > Edit Configurations > Defaults > py.test > Additional Arguments` and add `--capture=no` (`-s`). Verbosity can also be increased by adding one or more `-v`.  


### Django

* Testing of the GMN Django web app is based on pytest and [pytest-django](https://pytest-django.readthedocs.io/en/latest/).

* The tests use `settings_test.py` for GMN and Django configuration.

* Pytest-django forces `settings.DEBUG` to `False` in `pytest_django/plugin.py`. To set `settings.DEBUG`, override it close to where it will be read, e.g., wit `@django.test.override_settings(DEBUG=True)`.


#### Django database test fixture

After changing any of the ORM classes in models.py, the database test fixture must be regenerated. This will often cause sample files to have to be updated as well.

Regenerated the fixture files:

    $ pytest --fixture-regen
    $ ./d1_python/gmn/src/d1_gmn/tests/mk_db_fixture.py

Fixtures can be loaded directly into the test database from the JSON files but it's much faster to keep an extra copy of the db as a template and create the test db as needed with Postgres' "create database from template" function. So we only load the fixtures into a template database and reuse the template. This is implemented in `./conftest.py`.

Note that science object bytes are stored on disk, so they are not captured in the db fixture. If a test needs get(), getChecksum() and replica() to work, it must first create the correct file in GMN's object store or mock object store reads. The bytes are predetermined for a given test PID. See `d1_test.d1_test_case.generate_reproducible_sciobj_str()` and `d1_gmn.app.util.sciobj_file_path()`.


### Setting up the development environment

These instructions are tested on Linux Mint 18 and should also work on close derivatives.

Install packaged dependencies:

    $ sudo apt-get update
    $ sudo apt-get -fy dist-upgrade
    $ sudo apt-get install -y subversion python-setuptools python-dev \
    libssl-dev postgresql-server-dev-all git

Download the source from GitHub:

    $ git clone https://github.com/DataONEorg/d1_python.git

Add the DataONE packages to the Python path, and install their dependencies:

    $ sh $D1ROOT/dev_tools/develop.sh

Run the following commands, except, change the "createuser" line to:

    $ sudo -u postgres createuser <youruser> ($ whoami)

    https://pythonhosted.org/dataone.generic_member_node/setup-local-postgresql.html

Run the following commands (all sections), except, change the location for openssl.cnf, so the line that copies it becomes:

    $ sudo cp /home/dahl/d1_python/d1_mn_generic/src/deployment/openssl.cnf .

  https://pythonhosted.org/dataone.generic_member_node/setup-local-authn-ca.html

Run the tests and verify that they all pass:

    $ pytest

Set up credentials for working with the DataONE account on PyPI:

Edit `~/.pypirc`:

    [server-login]
    username: dataone
    password: <secret>

### Creating a new release

#### Updating dependencies

Update all packages managed by pip:

    $ cd d1_python
    $ sudo ./dev_tools/src/d1_dev/pip-update-all.py

The DataONE Python stack specifies fixed versions of all its dependencies. This ensures that a stack deployed to production matches one that passed the tests. As updating the versions in the `setup.py` files manually is time consuming and error prone, a script is included that automates the task. The script updates the version information for the dependencies in the `setup.py` files to match the versions of the currently installed dependencies. Run the script with:

    $ cd d1_python
    $ src-sync-dependencies.py . <version>

The `<version>` argument specifies what the version will be for the release. E.g., `"2.3.1"`. We keep the version numbers in sync between all of the packages in the d1_python git repository, so only one version string needs to be specified.

Check that there are no package version conflicts:

    $ pip check

Some sample files contain the version tag and must be updated when the version changes.  

    $ pytest -xvs --sample-ask

Commit and push the changes, and check the build on Travis.

#### Building the release packages

After successful build, clone a fresh copy, which will be used for building the release packages:

    $ cd ~
    $ rm -rf ~/d1_python_build
    $ git clone git@github.com:DataONEorg/d1_python.git d1_python_build

Building the release packages from a fresh clone is a simple way of ensuring that only tracked files are released. It is a workaround for the way setuptools works, which is basically that it vacuums up everything that looks like a Python script in anything that looks like a package, which makes it easy to publish local files by accident.

Build and publish the packages:

    cd ~/d1_python_build
    setup-all.py --root . bdist_wheel upload


### Building the documentation

When `d1_python` is pushed to GitHub, a signal is sent by GitHub to [ReadTheDocs.org](https://readthedocs.org/), which automatically retrieves the new version of the project from GitHub, builds the documentation and makes it available at

http://dataone-python.readthedocs.io/en/latest/

So it is not absolutely necessary to have a local build environment set up for the documentation, but building locally provides faster feedback when making changes that need to be checked before publishing.  

### Troubleshooting

Clear out the installed libraries and reinstall:

    $ sudo rm -rf /usr/local/lib/python2.7/dist-packages/d1_*
    $ sudo nano /usr/local/lib/python2.7/dist-packages/easy-install.pth
    Remove all lines that are: dataone.*.egg and that are paths to your d1_python.
