DataONE Generic Member Node
===========================

\

==================== ==============================================
Component            Tested version(s)
==================== ==============================================
Python               2.6
subversion           \
==================== ==============================================


The distribution of GMN is currently Subversion based. This makes it easy to
keep up to date with changes.

  Install Subversion::

    $ sudo apt-get install subversion

  Create and/or enter the folder where you wish to install GMN::

    $ sudo -s
    # mkdir -p /var/local/dataone
    # cd /var/local/dataone

  Download GMN::

    $ sudo svn co https://repository.dataone.org/software/cicore/trunk/mn/d1_mn_generic/ gmn


Configure GMN
~~~~~~~~~~~~~

  Edit: ``/var/local/dataone/mn_generic/service/settings_site.py``

  * The NODE_IDENTIFIER is configured later, in the :doc:`setup-registration`
    step.

  * Set DEBUG = False

  * Replace the name and email address in ADMINS with the name and email address
    for a person that should be notified if there are any issues. Additional
    administrators can be added.

  * In the DATABASES section, set the password to what was specified during the
    PostgreSQL installation step: :doc:`setup-postgresql`.


Initialize the database
~~~~~~~~~~~~~~~~~~~~~~~

  ::

    $ cd /var/local/dataone/mn_generic/service
    $ python manage.py syncdb


Set filesystem permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~

  * Make sure that all files under ``/var/local/dataone`` can be read by the
    user account under which Apache runs (www-data by default)
  * Make sure that the log files can be written by the Apache user account.
  * When using SQLite (currently unsupported), make sure that the SQLite
    database file can be written by the Apache user account.


Set server to the UTC timezone (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GMN translates incoming date-times to UTC and provides outgoing date-times in
UTC. Because of this, it may also convenient to run the server in UTC, so that
server related date-times, such as the ones in logs, match up with date-times
stored in the database and provided in REST responses.

  ::

    $ dpkg-reconfigure tzdata


:doc:`setup-registration`
