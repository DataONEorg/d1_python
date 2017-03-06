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

## Code style

We try to follow [PEP8](https://www.python.org/dev/peps/pep-0008/), with the two
main exceptions being that we use two spaces per indent and two lines between
functions.

To help keep code annotations accurate and commit diffs minimal, we use
[YAPF](https://github.com/google/yapf) to format Python scripts before
committing to GitHub. The style configuration file for YAPF is included in this
repository, at `./yapf_style.cfg`.

Contributors are strongly encouraged to set up automatic YAPF formatting before
commit using a Git hook. A configuration file for [pre-commit](pre-commit.com)
is included in this repository. To set up automatic formatting:

    $ sudo pip install pre-commit
    $ pre-commit autoupdate
    $ pre-commit install

This will use the included YAPF configuration file.
