Installing d1_common_python
===========================

The simplest way to utilize the library is to check out the source from
`subversion`_ and work from there. This makes it easy to keep up to date with
changes.

A package will be released at some point in the future once things stabilize
a bit.

To set the library up in ``/var/local/dataone/d1_common_python`` on Linux, using
`Bash`_ (which is often the default shell)::

  $ sudo -s
  # mkdir -p /var/local/dataone
  # cd /var/local/dataone
  # svn co https://repository.dataone.org/software/cicore/trunk/d1_common_python d1_common_python
  # cd d1_common_python/d1_common/src
  # python setup.py develop
  $ exit

To update your copy of the library::

  $ cd /var/local/dataone/d1_common_python
  $ svn update

.. _subversion: http://subversion.tigris.org/
.. _Bash: http://www.gnu.org/software/bash/
