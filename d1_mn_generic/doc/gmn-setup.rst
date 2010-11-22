Generic Member Node Setup
=========================

.. note::
  These instructions focus on installing the DAAC instance of the Generic Member
  Node (GMN). GMN can be configured as a standalone Member Node or as an adapter
  for an existing repository. These instructions desribe how to install GMN as
  an adapter.

Terminology
-----------

:GMN:
  Generic Member Node.

:MN:
  DataONE Member Node.

:CN:
  DataONE Coordinating Node.

:SciData:
  An object (file) that contains scienctific observational data.

:SciMeta:
  An object (file) that contains information about a SciData object.

:SysMeta:
  An object (file) that contains system level information about a SciData or a
  SciMeta object.

:Adaptee:
  A 3rd party system that uses GMN to expose its data through DataONE.


System overview
---------------

1.
  GMN is installed on a physical or virtual machine. Network connectivity is
  arranged so that GMN can be reached from the Internet and from the adaptee and
  can itself reach the adaptee's storage facilities.

#.
  The adaptee calls into GMN with a REST call for each object that it wants to
  expose through DataONE. Each REST call provides GMN with either a full SciMeta
  or SciData object (in standalone mode) or URL to such an object (in adapter
  mode), and a corresponding SysMeta object.

#.
  GMN will then serve collection related calls directly from its database.

#.
  When the bytes of a SciData or SciMeta object are requested, GMN serves the
  object from local storage in standalone mode or uses the URL stored in its
  database to retrieve the object from the adaptee's storage facilities and
  streams it out, acting as a streaming proxy in adapter mode.
  

System requirements
===================

Hardware
--------

============ =================================
Component    Minimum
============ =================================
RAM          Workload dependent
CPU          Workload dependent
Disk         Workload dependent
Network      Workload dependent
============ =================================


Software
--------

OS and Environment
``````````````````

Required pakages that are not installed by default in Ubuntu 9.10.

==================== ==============================================
Component            Minimum Version
==================== ==============================================
Ubuntu               9.10+
Apache               2
Python               2.6
sqlite               3
gcc                  \
apache2              \
libapache2-mod-wsgi  \
apache2-threaded-dev \
openssh-server       \
libxml2-dev          \
libxslt-dev          \
python-dev           2.6
python-django        1.1
python-setuptools    \
python-dateutil      \
sqlite3              \
subversion           \
==================== ==============================================


Python Modules
``````````````

======== ========================================
Module   Minimum Version
======== ========================================
iso8601  \
Lxml     2.2.6
======== ========================================


Installation
============


Install dependencies
--------------------

Packages::

  $ sudo apt-get install gcc apache2-threaded-dev openssh-server libxml2-dev libxslt-dev python-dev python-django libapache2-mod-wsgi python-setuptools python-dateutil apache2 sqlite3 subversion
  
Python dependencies::

  $ sudo easy_install iso8601 lxml

PyXB XML bindings generator::

  $ wget http://surfnet.dl.sourceforge.net/project/pyxb/pyxb/1.1.2%20%28Beta%29/PyXB-base-1.1.2.tar.gz
  $ tar xzf PyXB-base-1.1.2.tar.gz
  $ cd PyXB-1.1.2
  $ sudo python setup.py install


Install GMN DAAC
----------------

The distribution of GMN is SVN based.

Create and/or enter the folder where you wish to install GMN DAAC::

  $ cd /var/local

Download the GMN DAAC "package"::

  $ sudo svn co https://repository.dataone.org/software/python_products/mn_daac mn_daac

Enter the DataONE Common library for Python::

  $ cd mn_daac/d1_common

Install the library::

  $ sudo python setup.py develop
  
Enter the DataONE Client library for Python::

  $ cd ../d1_libclient

Install the library::

  $ sudo python setup.py develop


Install the GMN service
-----------------------

Edit the gmn.cfg file and change *name* and *identifier* to values that are
unique for this instance of GMN::

  $ cd ../mn_generic/service
  $ vi gmn.cfg
  
Setup GMN::

  $ sudo ../install/config.py

config.py performs the following tasks:

* Set up mod_wsgi entry for GMN.
* Create sqlite database file for GMN.
* Make sure logfile can be written by group www-data.
* Make sure db file and PARENT FOLDER of db file is writeable by www-data.
* Copy fixed config values from .cfg file to database.
* Update GMN version from SVN revision number.
* Restart Apache.

