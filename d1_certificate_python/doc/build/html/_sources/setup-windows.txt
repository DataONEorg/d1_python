Build and install for Windows
=============================

Compiling
~~~~~~~~~

.. note:: For Windows, the DataONE x509v3 Certificate Extractor is supplied as a
  precompiled binary so it is typically not necessary to perform the steps in this
  section.

\

  Download and install MinGW from http://sourceforge.net/projects/mingw/files/

Distutils contains configuration scripts for the various supported compilers.
The script called `cygwinccompiler.py` covers compilation both with Cygwin and
MinGW. However, as of 5/2/2012, it is outdated in respect to the MinGW compiler
and needs a small adjustment.

  Edit the MinGW compiler configuration file::

    C:\Python27\Lib\distutils\cygwinccompiler.py

  Remove all instances of `-mno-cygwin`.

The OpenSSL library must be installed and compiled.

  Download the OpenSSL source package from http://www.openssl.org/source/

  Follow instructions in the OpenSSL source package to compile the library
  for Windows.

The Python header include path in the extension C file must be modified for
the default location of Python on Windows (C:\Python27).


  Edit `d1_x509v3_certificate_extractor.c`.

  Change the Python include to `#include <Python.h>`.

Paths to the OpenSSL include and lib directories must be added to the setup
script.

  Edit `setup.py`.

  Add the OpenSSL include and lib directories. For example::

    module1 = Extension('d1_x509v3_certificate_extractor',
      sources=['d1_x509v3_certificate_extractor.c'],
      include_dirs=[r'C:\dev\10_32\openssl\include'],
      library_dirs=[r'C:\dev\10_32\openssl\lib'])

Compile the extension.

  Open a command prompt at the location of the `setup.py` file.

  Add a path to MinGW (in the default location)::

    > set path=%path%;c:\MinGW\bin

  Built the extension with MinGW::

    > c:\Python27\python.exe setup.py build -cmingw32
