Troubleshooting
===============

Psycopg2 gives "can't adapt" errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The version of Psycopg2 that was installed by default was not compatible.

Try uninstalling the default version and installing a specific version. The
version referenced below had been found to work well with PostgreSQL 8.4.10.

::

  $ sudo apt-get remove python-psycopg2
  $ mkdir ~/install
  $ cd ~/install
  $ wget http://initd.org/psycopg/tarballs/PSYCOPG-2-4/psycopg2-2.4.2.tar.gz
  $ tar xzf psycopg2-2.4.2.tar.gz
  $ cd psycopg2-2.4.2
  $ sudo python setup.py install

Another option is to try to install Psycopg2 via easy_install::

  $ sudo easy_install -m psycopg2

To remove a version of Psycopg2 that was installed with easy_install::

  $ sudo rm -rf /usr/lib/python2.7/dist-packages/psycopg2
