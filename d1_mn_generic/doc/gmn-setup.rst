GMN Setup
=========

.. note::
  Dryad: For now, this document is focused on the Dryad MN implementation. I
  plan on splitting Dryad specific information into a separate document later.

.. note::
  Dryad: Using GMN to expose Dryad objects is a short-term solution, intended
  only to meet NSF obligations and provide an initial test of GMN. No more than
  1 week of effort should be spent on it. If more time is required, this
  approach should be scrapped, and the resources should be directed towards the
  long-term implementation.

.. note::
  Dryad: Package objects (which contain references to multiple data files, but
  don't contain the actual files) will not be implemented in this process -- we
  will address packaging in the next revision.

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
  expose through DataONE (object registration).

#.
  The adaptee creates a SysMeta objects for each object it registers and makes
  it available to GMN. SysMeta objects are not registered -- it is assumed that
  a SysMeta object is available for each SciData and SciMeta object.

#.
  When an object is registered with GMN, the registration entry is queued for
  asynchronous processing and the call returns immediately.

#.
  At regular intervals, GMN processes the queue of object registrations and
  registers them in its database.

#.
  GMN will then serve collection related calls directly from its database.

#.
  When the bytes of a SciData or SciMeta object are requested, GMN uses the URL
  stored in its database to retrieve the object from the adaptee's storage
  facilities and streams it out, acting as a streaming proxy.

#.
  When SciMeta or the bytes of SciMeta are requested for a SciData object, the
  stored association is used for finding the related data. This also works the
  other way around.

#.
  When SysMeta objects are requested for for a SciMeta or SciData object, GMN
  deduces the SysMeta URL from the SciMeta or SciData URL and streams the object
  out as described for SciData and SciMeta.
  

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

==================== ==============================================
Component            Minimum Version
==================== ==============================================
Ubuntu               9.10+
Apache               2
Python               2.6
sqlite               3
apache2-threaded-dev (required for building mod_wsgi)
mod_wsgi             (from source)
gcc                  (required for building lxml)
python-dev           (required for building lxml and mod_wsgi)
libxml2-dev          (required for building lxml)
libxslt-dev          (required for building lxml)
libz-dev             (required for building lxml)
==================== ==============================================


Python Module
`````````````

======== ========================================
Module   Minimum Version
======== ========================================
Django   1.1
iso8601  \
Lxml     2.2.6
======== ========================================


Check Versions
``````````````

GCC::

  $ gcc -v

Python::

  $ python --version

Django::

  $ python
  Python 2.6.4 (r264:75706, Dec  7 2009, 18:43:55)
  [GCC 4.4.1] on linux2
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import django
  >>> django.VERSION
  (1, 1, 1, 'final', 0)

Lxml::

  $ python
  Python 2.6.4 (r264:75706, Dec  7 2009, 18:43:55)
  [GCC 4.4.1] on linux2
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import lxml

sqlite3::

  $ python
  Python 2.6.4 (r264:75706, Dec  7 2009, 18:43:55)
  [GCC 4.4.1] on linux2
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import sqlite3

dateutil::

  $ python
  Python 2.6.4 (r264:75706, Dec  7 2009, 18:43:55)
  [GCC 4.4.1] on linux2
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import dateutil


Installation
============

Install OS components
---------------------

::

# apt-get install gcc python-setuptools python-dateutil apache2 apache2-threaded-dev sqlite3 openssh-server python-setuptools libxml2-dev libxslt-dev python-dev

Install mod_wsgi
----------------

We use mod_wsgi for serving the GMN application with Apache.

Get mod_wsgi from the SVN head::

  svn checkout http://modwsgi.googlecode.com/svn/trunk/ modwsgi

Compile and install mod_wsgi::

  $ ./configure
  # make install


Install GMN
-----------

Download and install GMN and dependencies::

  # easy_install https://repository.dataone.org/software/cicore/trunk/mn_service/dist/Generic_Member_Node_GMN_-0.1-py2.6.egg


Setup GMN
---------

Running the following script performs the following tasks:

* Set up mod_wsgi for GMN.
* Create an empty sqlite3 database.
* Populate sqlite3 database with a few initial items.
* Restart Apache

* Make sure logfile can be written by group www-data.
* Make sure db file and PARENT FOLDER of db file is writeable by www-data.



::

  # ./config.py
  

Testing GMN
-----------

In a browser, open http://127.0.0.1/mn/log/ The installation is OK so
far if there are no errors returned.
