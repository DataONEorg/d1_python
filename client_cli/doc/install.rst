Installing the DataONE CLI
==========================

.. include:: overview.rst

Install
~~~~~~~

The CLI is distributed via PyPI, the Python Package Index.

Set up OS packages required by some of the CLI's PyPI distributed
dependencies. This includes a build environment for DataONE Python extensions.

::

  $ sudo apt install --yes build-essential python-dev libssl-dev \
  libxml2-dev libxslt-dev openssl curl

Install pip::

  $ sudo apt install --yes python-pip; sudo pip install pip --upgrade

Install the CLI from PyPI::

  $ sudo pip install dataone.cli
