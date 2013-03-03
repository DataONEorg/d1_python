Install and configure PostgreSQL
================================

:term:`Django`, on which GMN is built, supports :term:`PostgreSQL`,
:term:`SQLite3`, :term:`MySQL` and :term:`Oracle`. However, GMN currently
supports only PostgreSQL and SQLite3. GMN does not support MySQL and is untested
with Oracle.

This section describes how to set up PostgreSQL for GMN. The section can be
skipped if SQLite3 will be used. If so, modify the database setting in the GMN
``settings_site.py`` file as described in that file.

  Install PostgreSQL::

    $ sudo apt-get --yes install postgresql

In PostgreSQL, the user with unlimited access is called the superuser. The
superuser does not have a password by default.

  Set the password for the superuser::

    $ sudo su postgres -c psql template1
    postgres=# alter user postgres with encrypted password '<your superuser password>';
    postgres=# <ctrl-d>

PostgreSQL runs under a separate user account called postgres.

  Set the password of the postgres user account to match the one of the
  superuser::

    $ sudo passwd -d postgres
    $ sudo su postgres -c passwd

  When prompted for the password, enter <your superuser password>.

Under Ubuntu, PostgreSQL uses Ident-based authentication by default. Change
this to md5.

  Edit ``pg_hba.conf``::

    $ sudo pico /etc/postgresql/8.4/main/pg_hba.conf

  Change::

    local   all         all                               ident

  To::

    local   all         all                               md5

  Restart PostgreSQL::

    $ sudo service postgresql-8.4 restart

  Create GMN user::

    $ sudo -u postgres createuser gmn
    Shall the new role be a superuser? (y/n) n
    Shall the new role be allowed to create databases? (y/n) n
    Shall the new role be allowed to create more new roles? (y/n) n

  Create a database for GMN::

    $ sudo -u postgres createdb -E UTF8 gmn

  Set the password for the GMN user::

    $ sudo -u postgres psql template1
    template1=# ALTER USER gmn WITH ENCRYPTED password '<your gmn user password>';
    template1=# <ctrl-d>
