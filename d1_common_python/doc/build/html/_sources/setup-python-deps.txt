Python dependencies
===================

Minimum component versions
--------------------------

==================== =================
Component            Minimum Version
==================== =================
python-setuptools    \
minixsv              \
python-dateutil      \
python-iso8601       \
python-dev           2.6
libxml2-dev          \
libxslt-dev          \
Lxml                 2.2.6
PyXB                 \
==================== =================


Install :term:`setuptools`::

  $ sudo easy_install python-setuptools


Install :term:`minixsv`::

  $ sudo easy_install minixsv


Install :term:`python-dateutil`::

  $ sudo easy_install python-dateutil
    

Install :term:`python-iso8601`::

  $ sudo easy_install iso8601
  

Install :term:`lxml`::

  $ sudo apt-get install gcc python-dev libxml2-dev libxslt-dev
  $ sudo easy_install lxml


Install :term:`PyXB`::

  $ mkdir ~/install
  $ cd ~/install
  $ wget http://surfnet.dl.sourceforge.net/project/pyxb/pyxb/1.1.2%20%28Beta%29/PyXB-base-1.1.2.tar.gz
  $ tar xzf PyXB-base-1.1.2.tar.gz
  $ cd PyXB-1.1.2
  $ sudo python setup.py install
