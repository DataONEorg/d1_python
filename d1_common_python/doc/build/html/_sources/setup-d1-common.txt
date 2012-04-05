DataONE Common Library for Python
=================================

The distribution of DataONE Common Library for Python is currently
:term:`Subversion` based. This makes it easy to keep up to date with changes. A
package will be released at some point in the future once things stabilize a
bit.

Install Subversion::

  $ sudo apt-get install subversion


Install DataONE Common Library for Python
-----------------------------------------

To set the library up in ``/var/local/dataone/d1_common_python`` using
:term:`Bash` (which is often the default shell)::

  $ sudo -s
  # mkdir -p /var/local/dataone
  # cd /var/local/dataone
  # svn co https://repository.dataone.org/software/cicore/trunk/d1_common_python d1_common_python
  # cd d1_common_python/src/
  # python setup.py develop
