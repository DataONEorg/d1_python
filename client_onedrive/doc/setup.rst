Installation
============

Microsoft Windows
~~~~~~~~~~~~~~~~~

1. Download the `latest ONEDrive for Windows setup
<https://repository.dataone.org/software/cicore/trunk/itk/d1_client_onedrive/src/onedrive-setup-2.0.0RC1.exe>`_.

#. Start the setup and follow the prompts.

#. Start ONEDrive from the Windows Start menu.

#. See :doc:`run` for notes on how to customize and access ONEDrive.

By default, ONEDrive uses the drive letter "O:". If this drive letter is already in use, it can be changed in the ``settings.py`` file.


Mac OS X
~~~~~~~~

1. Install FUSE

Development of ONEDrive on OS X has been done using the `Fuse for OS X`_ distribution. Download the latest installer (currently 2.5.4) and follow the instructions to install.

#. Install Python dependencies

fusepy_ provides the Python bindings to the FUSE library. To install fusepy, use the commands::

  $ cd Downloads
  $ git clone git://github.com/terencehonles/fusepy.git fusepy
  $ cd fusepy
  $ sudo python setup.py install


#. Install ONEDrive

There is currently no setup script for ONEDrive, so installation means simply downloading to a local folder::

  $ cd ~/opt
  $ svn co https://repository.dataone.org/software/cicore/trunk/itk/d1_client_onedrive
  $ cd d1_client_onedrive


* Set PYTHONPATH to include d1_common_python/src and d1_libclient_python/src
* On OS X, set DYLD_LIBRARY_PATH=/usr/lib:$DYLD_LIBRARY_PATH
* Make sure option 'user_allow_other' is set in /etc/fuse.conf.

If the library search path is incomplete, an exception such as the following may occur::

  OSError: dlopen(/opt/local/lib/libfuse.dylib, 6): Symbol not found: _iconv
    Referenced from: /opt/local/lib/libfuse.dylib

To work around this, run ``onedrive.py`` with::

  export DYLD_LIBRARY_PATH=/usr/lib:$DYLD_LIBRARY_PATH


.. _`Fuse for OS X`: http://osxfuse.github.com/

.. _fusepy: https://github.com/terencehonles/fusepy


Linux
~~~~~

Make sure the system is up to date::

  sudo -H bash -c '
    apt update --yes && apt dist-upgrade --yes
  '

* Reboot if necessary.

Set up server packages:

* The build environment for DataONE Python extensions
* Commands used in the install

::

  $ sudo apt install --yes build-essential python-dev libxml2-dev \
  libxslt-dev

Install pip::

  $ sudo apt install --yes python-pip; sudo pip install pip --upgrade;

Install ONEDrive, and its dependencies from PyPI, into a Python virtual environment. The virtual environment is set up under onedrive_bin in the user's home folder.

::

  $ sudo pip install virtualenv;
  $ cd; mkdir onedrive_bin; virtualenv --distribute onedrive_bin;
  cd onedrive_bin; . bin/activate; pip install dataone.onedrive

* Press ctrl-d to exit the virtualenv.

ONEDrive expects to find a workspace.xml file in your home folder. Copy one of the example workspaces there::

  $ cp onedrive_bin/workspace.xml ~

By default, ONEDrive uses a folder named "one" in your home folder as the mount point. Create it::

  $ mkdir ~/one

Start ONEDrive::

  $ ~/onedrive_bin/bin/onedrive

Open ~/one to access your DataONE objects.
