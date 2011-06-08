DataONE Client Library for Python
=================================

First, install :term:`DataONE Common Library for Python` according to the
instructions in the documentation for that project. It is a dependency of
:term:`DataONE Client Library for Python`.

The distribution of DataONE Common Library for Python is currently
:term:`Subversion` based. This makes it easy to keep up to date with changes. A
package will be released at some point in the future once things stabilize a
bit.

Install Subversion::

  $ sudo apt-get install subversion


Install DataONE Client Library for Python
-----------------------------------------

To set the library up in ``/var/local/dataone/d1_client_python`` using
:term:`Bash` (which is often the default shell)::

  $ sudo -s
  # mkdir -p d1_client_python
  # cd /var/local/dataone
  # svn co https://repository.dataone.org/software/cicore/trunk/d1_client_python d1_client_python
  # cd d1_client_python/d1_client/src
  # python setup.py develop

To update your copy of the library::

  $ cd /var/local/dataone/d1_client_python
  $ svn update
