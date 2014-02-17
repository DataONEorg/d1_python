Installing DataONE Common Library for Python
============================================

:term:`DataONE Common Library for Python` is distributed via PyPI, the Python
Package Index.

Windows
=======

1. If you do not already have a working 32-bit Python 2.7 environment, download
   the latest 32-bit Python 2.7 Windows installer from
   http://www.python.org/download/ and install it.

#. In ``Control Panel | Classic View | System | Advanced | Environment Variables``,
   add ``;C:\Python27;C:\Python27\Scripts`` to the end of the Path.

#. Install pip::

   > python -c "import urllib2; exec(urllib2.urlopen('https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py').read())"
   > easy_install pip

#. Open a Command Prompt.

#. Install PyXB::

   $ sudo pip install pyxb==1.2.3

#. Install the DataONE Common Library for Python and dependencies::

   > pip install dataone.common


Linux
=====

1. Install pip (Python package installer)::

   $ sudo apt-get --yes install python-pip; sudo pip install pip --upgrade;

#. Install PyXB::

   $ sudo pip install pyxb==1.2.3

#. Install the DataONE Common Library for Python and dependencies::

   $ sudo pip install dataone.common
