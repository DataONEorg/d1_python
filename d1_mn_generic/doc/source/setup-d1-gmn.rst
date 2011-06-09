Step 8: DataONE Generic Member Node
===================================

==================== ==============================================
Component            Minimum Version
==================== ==============================================
Python               2.6
sqlite               3
subversion           \
==================== ==============================================



Install the GMN service
-----------------------


sudo apt-get install sqlite3


The distribution of GMN is currently Subversion based. This makes it easy to
keep up to date with changes. A package will be released at some point in the
future once things stabilize a bit.

Install Subversion::

  $ sudo apt-get install subversion





Create and/or enter the folder where you wish to install GMN DAAC::

  $ cd /var/local/dataone

Download the GMN DAAC "package"::

  $ sudo svn co https://repository.dataone.org/software/python_products/mn gmn

gmn.cfg.template had that in there and there wasn't a gmn.cfg file, so I cp'd
the file and modified it, only touching the identifier and name as it says to in
the build docs

Edit the gmn.cfg file and change *name* and *identifier* to values that are
unique for this instance of GMN::

  $ cd gmn/service
  $ vi gmn.cfg

Setup GMN::

  $ sudo ../install/config.py

config.py performs the following tasks:

* Create sqlite database file for GMN.
* Make sure logfile can be written by group www-data.
* Make sure db file and parent folder of db file is writeable by www-data.
* Copy fixed config values from .cfg file to database.
* Update GMN version from SVN revision number.


From nick:

  $ cd /var/local
  $ sudo svn co https://repository.dataone.org/software/python_products/mn_daac mn
