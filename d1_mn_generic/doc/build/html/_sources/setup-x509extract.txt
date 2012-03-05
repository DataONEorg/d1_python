X.509 extract
=============

GMN includes a Python extension that interfaces with the :term:`OpenSSL`
library to extract DataONE session information from X.509 client side
certificates.

  Install the GNU Compiler Collection (GCC)::

    $ sudo apt-get install gcc

  Install the development version of Python::

    $ sudo apt-get install python-dev

  Install the OpenSSL library::

    $ sudo apt-get install openssl

  Build and install the Python extension::

    $ cd /var/local/dataone/mn_generic/x509_extract
    $ sudo python setup.py install

:doc:`setup-d1-gmn`
