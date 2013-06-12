DataONE Client Library for Python
=================================

:term:`DataONE Common Library for Python` is distributed via PyPI, the Python
Package Index.

  Set up server packages:

  * The build environment for DataONE Python extensions and lxml
  * Commands used in the install

  ::

    $ sudo apt-get --yes install build-essential python-dev libssl-dev \
    libxml2-dev libxslt-dev openssl

  Install pip (Python package installer)::

    $ sudo apt-get --yes install python-pip; sudo pip install pip --upgrade;

  Install the DataONE Client Library for Python and all its dependencies. This
  will also automatically build several Python C extensions::

    $ sudo pip install dataone.libclient


The library can be tested by running one of the included usage examples. The
examples can be found in the `dist-packages` folder, for instance::

  /usr/local/lib/python2.6/dist-packages/examples/
