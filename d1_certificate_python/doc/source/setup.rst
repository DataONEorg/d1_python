Build and install
=================

The DataONE Certificate Extensions are Python extensions implemented in C. They
depend on the OpenSSL C library. When installing the extensions, they are
automatically compiled, so the following instructions set up a working build
environment before installing the extensions from PyPI.

Prepare the build environment::

  $ sudo apt-get --yes install build-essential python-dev libssl-dev \
  python-pip; sudo pip install pip --upgrade;

Install::

  $ sudo pip install dataone.certificate_extensions
