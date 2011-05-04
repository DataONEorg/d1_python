Installing d1_libclient_python
==============================

First, install ``d1_common_python`` according to the instructions in the
documentation for that project. It is a dependency of ``d1_libclient_python``.

The simplest way to utilize the library is to check out the source from
`subversion`_ and work from there. This makes it easy to keep up to date with
changes.

A package will be released at some point in the future once things stabilize
a bit.

To set the library up in ``/var/local/dataone/d1_client_python`` on Linux, using
`Bash`_ (which is often the default shell)::

  $ sudo -s
  # mkdir -p d1_client_python
  # cd /var/local/dataone
  # svn co https://repository.dataone.org/software/cicore/trunk/d1_client_python d1_client_python
  # cd d1_client_python/d1_client/src
  # python setup.py develop
  $ exit

To update your copy of the library::

  $ cd /var/local/dataone/d1_client_python
  $ svn update

.. _subversion: http://subversion.tigris.org/
.. _Bash: http://www.gnu.org/software/bash/


