DataONE Generic Member Node
===========================

\

==================== ==============================================
Component            Tested version(s)
==================== ==============================================
Python               2.6
subversion           \
==================== ==============================================


GMN is currently distributed as a zip file and as Subversion repository.
Select one of the distribution methods below.

Zip file
~~~~~~~~

  Create and/or enter the folder where you wish to install GMN::

    $ sudo -s
    # mkdir -p /var/local/dataone
    # cd /var/local/dataone

  Download GMN from zip file and install::

    $ wget <zip path>
    $ gunzip x <zip>


Subversion
~~~~~~~~~~

  Install Subversion::

    $ sudo apt-get install subversion

  Create and/or enter the folder where you wish to install GMN::

    $ sudo -s
    # mkdir -p /var/local/dataone
    # cd /var/local/dataone

  Download GMN from the Subversion repository::

    $ sudo svn co https://repository.dataone.org/software/cicore/tags/D1_MN_GENERIC_V1.0.0-RC1/ gmn



Configure GMN
~~~~~~~~~~~~~

  Create a copy of the site settings template::

    $ cd /var/local/dataone/gmn/src/service
    $ cp settings_site_template.py settings_site.py

  Edit: ``/var/local/dataone/gmn/src/service/settings_site.py``

  * The NODE_IDENTIFIER is configured later, in the :doc:`setup-registration`
    step.

  * Replace the name and email address in ADMINS with the name and email address
    for a person that should be notified if there are any issues. Additional
    administrators can be added.

  * In the DATABASES section, set the password to what was specified during the
    PostgreSQL installation step: :doc:`setup-postgresql`.


Initialize the database
~~~~~~~~~~~~~~~~~~~~~~~

  ::

    $ cd /var/local/dataone/gmn/src/service
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
