Step 10: DataONE Generic Member Node
===================================

\

==================== ==============================================
Component            Tested version(s)
==================== ==============================================
Python               2.6
sqlite               3
subversion           \
==================== ==============================================


Install packaged dependencies for GMN
-------------------------------------

GMN uses the SQLite database.

Install SQLite::

  sudo apt-get install sqlite3


Install Subversion:

The distribution of GMN is currently Subversion based. This makes it easy to
keep up to date with changes. A package will be released at some point in the
future once things stabilize a bit.

::

  $ sudo apt-get install subversion


Create and/or enter the folder where you wish to install GMN::

  $ sudo -s
  # mkdir -p /var/local/dataone
  # cd /var/local/dataone

Download GMN::

  $ sudo svn co https://repository.dataone.org/software/cicore/trunk/mn/d1_mn_generic/ gmn

Configure GMN:

Create the gmn.cfg file and change *name* and *identifier* to values that are
unique for this instance of GMN::

  $ sudo -s
  # cd /var/local/dataone/gmn/src/service
  # cp gmn.cfg.template gmn.cfg
  # vi gmn.cfg

Setup GMN:

  $ sudo -s
  # cd /var/local/dataone/gmn/src/service
  # sudo ../install/config.py

config.py performs the following tasks:

* Create sqlite database file for GMN.
* Make sure logfile can be written by group www-data.
* Make sure db file and parent folder of db file is writeable by www-data.
* Copy fixed config values from .cfg file to database.
* Update GMN version from SVN revision number.
