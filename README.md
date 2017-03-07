# d1_python

Python components for DataONE clients and servers.

## Releases on the Python Package Index (PyPI)

### v2 and v1 API

* [DataONE Generic Member Node](https://pypi.python.org/pypi/dataone.gmn)
* [DataONE Client Library for Python](https://pypi.python.org/pypi/dataone.libclient)
* [DataONE Common Library for Python](https://pypi.python.org/pypi/dataone.common)

### v1 API

* [DataONE Command Line Client (CLI)](https://pypi.python.org/pypi/dataone.cli)
* [DataONE Certificate Extensions](https://pypi.python.org/pypi/dataone.certificate_extensions)
* [DataONE Gazetteer](https://pypi.python.org/pypi/dataone.gazetteer)
* [DataONE ONEDrive](https://pypi.python.org/pypi/dataone.onedrive)
* [DataONE Test Utilities](https://pypi.python.org/pypi/dataone.test_utilities)
* [DataONE Ticket Generator](https://pypi.python.org/pypi/dataone.ticket_generator)
* [Google Foresite Toolkit](https://pypi.python.org/pypi/google.foresite-toolkit)

## Documentation

See [documentation on ReadTheDocs](http://dataone-python.readthedocs.io/en/latest/)

### v2 and v1 API

* [Overview](http://dataone-python.readthedocs.io/en/latest/)
* [DataONE Generic Member Node](http://dataone-python.readthedocs.io/en/latest/gmn/index.html)
* [DataONE Client Library for Python](http://dataone-python.readthedocs.io/en/latest/client/index.html)
* [DataONE Common Library for Python](http://dataone-python.readthedocs.io/en/latest/common/index.html)

### v1 API

* [DataONE Command Line Client (CLI)](http://dataone-python.readthedocs.io/en/latest/cli/index.html)
* [DataONE ONEDrive](http://dataone-python.readthedocs.io/en/latest/onedrive/index.html)
* [DataONE Test Utilities](http://dataone-python.readthedocs.io/en/latest/test/index.html)

## Contributing

Pull Requests (PRs) are very welcome! Before you start coding, feel free to reach out to us and let us know what you plan to implement. We might be able to point you in the right direction.

We try to follow [PEP8](https://www.python.org/dev/peps/pep-0008/), with the main exception being that we use two instead of four spaces per indent.

To help keep the style consistent and commit logs, blame/praise and other code annotations accurate, we use the following `pre-commit` hooks to automatically format and check Python scripts before committing to GitHub:

* [YAPF](https://github.com/google/yapf) - PEP8 formatting with DataONE modifications
* [Flake8](http://flake8.pycqa.org/en/latest/) - Lint, code and style validation
* [trailing-whitespace](git://github.com/pre-commit/pre-commit-hooks) - Remove trailing whitespace

Configuration files for `YAPF` and `Flake8` are included in this repository.

Contributors are strongly encouraged to set up the hooks before creating PRs. This can be done automatically, with [pre-commit](pre-commit.com), for which a configuration file has also been included.

To set up automatic formatting:

    $ sudo pip install pre-commit
    $ cd <a folder in the Git working tree for the repository>
    $ pre-commit autoupdate
    $ pre-commit install

Notes:

* If the `YAPF` or `trailing-whitespace` hooks modify the file that is being committed, the hooks will show as `Failed` and the commit is aborted. This provides an opportunity to examine the reformatted file and run the unit and integration tests again in order make sure the reformat did not break anything. A new commit can then be issued to commit the file. If no modifications have been made to the file, the commit then goes through, with the hooks showing a status of `Passed`.

* `Flake8` only performs validation, not formatting. If validation fails, the issues must be fixed in order to commit the file. The modifications may then trigger a new formatting by `YAPF` and/or `trailing-whitespace`, thus requiring a new commit.

* If desired, the number commits to issue can be reduced with workflow adjustments:

  * **trailing whitespace**: Use an editor that can strip trailing whitespace on save. E.g., for PyCharm, this setting is at `Editor > General > Strip trailing spaces on Save`.

  * **YAPF formatting**: Call `YAPF` manually on the file before commit. `YAPF` searches from current directory and up in the tree for configuration files. So, as long as current directory is in the repository root or below, `YAPF` should pick up and use the configuration that is included in the repository. To call `YAPF` manually, it can either be installed separately, or an alias can be set up to call the version that `pre-commit` has installed into its own venv.

  * **Flake8 validation**: the same procedure as for `YAPF` can be used, as `Flake8` searches for its configuration file in the same way. In addition, IDEs can typically do code inspections and tag issues directly in the UI, where they can be handled before commit.

* See the `YAPF` and `Flake8` config files at `./.style.yapf` and `./.flake8` for the formatting options we have selected.
