# d1_python

Python components for DataONE clients and servers.

See the [documentation on ReadTheDocs](http://dataone-python.readthedocs.io/en/latest/).

[![Build Status](https://travis-ci.org/DataONEorg/d1_python.svg?branch=master)](https://travis-ci.org/DataONEorg/d1_python)
[![Coverage Status](https://coveralls.io/repos/github/DataONEorg/d1_python/badge.svg?branch=master)](https://coveralls.io/github/DataONEorg/d1_python?branch=master)
[![PyPI version](https://badge.fury.io/py/dataone.common.svg)](https://badge.fury.io/py/dataone.common)

#### v2 and v1 API

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

#### v1 API

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

#### Contributing

Pull Requests (PRs) are welcome! Before you start coding, feel free to reach out to us and let us know what you plan to implement. We might be able to point you in the right direction.

We try to follow [PEP8](https://www.python.org/dev/peps/pep-0008/), with the main exception being that we use two instead of four spaces per indent.

To help keep the style consistent and commit logs, blame/praise and other code annotations accurate, we use the following `pre-commit` hooks to automatically format and check Python scripts before committing to GitHub:

* [YAPF](https://github.com/google/yapf) - PEP8 formatting with DataONE modifications
* [Flake8](http://flake8.pycqa.org/en/latest/) - Lint, code and style validation
* [trailing-whitespace](git://github.com/pre-commit/pre-commit-hooks) - Remove trailing whitespace

Configuration files for `YAPF` and `Flake8` are included in this repository.

Contributors are encouraged to set up the hooks before creating PRs. This can be done automagically with [pre-commit](pre-commit.com), for which a configuration file has also been included.

To set up automatic validation and formatting:

    $ sudo pip install pre-commit
    $ cd <a folder in the Git working tree for the repository>
    $ pre-commit autoupdate
    $ pre-commit install

Notes:

* If the `YAPF` or `trailing-whitespace` hooks modify any of the files being committed, the hooks will show as `Failed` and the commit is aborted. This provides an opportunity to examine the reformatted files and run the unit and integration tests again in order make sure the reformat did not break anything. Then, the modified files can then be staged and committed again. If no new modifications have been made, the commit then goes through, with the hooks showing a status of `Passed`.

* `Flake8` only performs validation, not formatting. If validation fails, the issues should be fixed before committing. The modifications may then trigger a new formatting by `YAPF` and/or `trailing-whitespace`, thus requiring the files to be staged and commited again.

* If desired, the number of extra staging and commits caused by reformatting and validation can be reduced with workflow adjustments:

  * **trailing whitespace**: Use an editor that can strip trailing whitespace on save. E.g., for PyCharm, this setting is at `Editor > General > Strip trailing spaces on Save`.

  * **YAPF formatting**: Call `YAPF` manually on the file before commit. `YAPF` searches from current directory and up in the tree for configuration files. So, as long as current directory is in the repository root or below, `YAPF` should pick up and use the configuration that is included in the repository. To call `YAPF` manually, it can either be installed separately, or an alias can be set up to call the version that `pre-commit` has installed into its own venv.

  * **Flake8 validation**: the same procedure as for `YAPF` can be used, as `Flake8` searches for its configuration file in the same way. In addition, IDEs can typically do code inspections and tag issues directly in the UI, where they can be handled before commit.

* See the `YAPF` and `Flake8` config files at `./.style.yapf` and `./.flake8` for the formatting options we have selected.
