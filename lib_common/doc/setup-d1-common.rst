Installing DataONE Common Library for Python
============================================

:term:`DataONE Common Library for Python` is distributed via PyPI, the Python Package Index.

Pip or another package manager such as apt may be used to install dependencies.

Note that versions available through package managers such as apt tend to lag significantly behind the latest versions, so it is recommended that Pip is used to manage dependencies. In order to avoid potential conflicts with system installed libraries, it is further recommended that a Virtual Environment or user installs of the dependencies are employed.


Windows
=======

1. If you do not already have a working 32-bit Python 3.6 environment, download
   the latest 32-bit Python 3.6 Windows installer from
   http://www.python.org/download/ and install it.

#. In ``Control Panel | Classic View | System | Advanced | Environment Variables``,
   add ``;C:\Python27;C:\Python27\Scripts`` to the end of the Path.

#. Install pip::

   > python -c "import urllib2; exec(urllib2.urlopen('https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py').read())"
   > easy_install pip

#. Open a Command Prompt.

#. Install the DataONE Common Library for Python and dependencies::

   > pip install dataone.common


Linux
=====

1. Install pip (Python package installer)::

   $ sudo apt install --yes python-pip; sudo pip install pip --upgrade;

#. Install the DataONE Common Library for Python and dependencies::

   $ sudo pip install dataone.common


Development
===========

To set up a virtual environment::

  pip install virtualenv
  virtualenv dataone_python
  source dataone_python/bin/activate
  pip install -U iso8601
  pip install -U pyxb
  pip install -U requests

Or as a user specific installation::

  pip install --user -U iso8601
  pip install --user -U pyxb
  pip install --user -U requests
