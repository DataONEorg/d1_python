Build and install
=================

The DataONE x509v3 Certificate Generator is a Python extension written in C. It
depends on the OpenSSL C library. A working GCC compiler environment and a
development version of Python must be present to compile the extension.

Install GCC and related tools::

  $ sudo apt-get install build-essential

Install the development version of Python::

  $ sudo apt-get install python-dev

Install the OpenSSL library::

  $ sudo apt-get install openssl

Build and install the x509v3 Certificate Extractor::

  $ sudo python setup.py install
