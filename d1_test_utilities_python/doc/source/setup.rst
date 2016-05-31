Build and install
=================

The :term:`DataONE Test Utilities for Python` are distributed via PyPI, the
Python Package Index.

  Set up server packages:

  * The build environment for DataONE Python extensions and lxml
  * Commands used in the install

  ::

    $ sudo apt-get --yes install build-essential python-dev libssl-dev \
    libxml2-dev libxslt-dev openssl

  Install pip (Python package installer)::

    $ sudo apt-get --yes install python-pip; sudo pip install pip --upgrade;

  Install the Test Utilities and their dependencies, including
  `Multi-Mechanize`_. This will also automatically build several Python C
  extensions::

    $ sudo pip install dataone.test_utilities


.. _`Multi-Mechanize`: http://multimechanize.com
