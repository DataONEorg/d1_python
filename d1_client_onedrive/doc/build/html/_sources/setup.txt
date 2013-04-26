Installation
============

The process for installing ONEDrive on OS X and Linux is similar:

1. Install FUSE
2. Install python dependencies
3. Install ONEDrive


Mac OS X
--------

1. Install FUSE

Development of ONEDrive on OS X has been done using the `Fuse for OS X`_
distribution. Download the latest installer (currently 2.5.4) and follow the
instructions to install.

2. Install Python dependencies

fusepy_ provides the Python bindings to the FUSE library. To install fusepy,
use the commands::

  $ cd Downloads
  $ git clone git://github.com/terencehonles/fusepy.git fusepy
  $ cd fusepy
  $ sudo python setup.py install


3. Install ONEDrive

There is currently no setup script for ONEDrive, so installation means simply
downloading to a local folder::

  $ cd ~/opt
  $ svn co https://repository.dataone.org/software/cicore/trunk/itk/d1_client_onedrive
  $ cd d1_client_onedrive


.. _Fuse for OS X:: http://osxfuse.github.com/

.. _fusepy:: https://github.com/terencehonles/fusepy


Linux
-----

TODO:: 
  Detail steps for setting up on linux, which will be the same as OS X
  except with the regular FUSE distro instead.


Windows
-------

TODO:: Need to setup a windows system and detail the steps.


Setting up the :term:`ONEDrive`.

