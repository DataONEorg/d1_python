PostgreSQL
==========

\

==================== ==============================================
Component            Tested version(s)
==================== ==============================================
PostgreSQL           8.4.10, 8.4.12
==================== ==============================================

:term:`Django`, on which GMN is built, is database agnostic. However, GMN
currently only supports :term:`PostgreSQL`. This section describes how to set up
PostgreSQL for GMN.

  Install PostgreSQL::

    $ sudo apt-get install postgresql

In PostgreSQL, the user with unlimited access is called the superuser. The
superuser does not have a password by default.

  Set the password for the superuser::

    $ sudo su postgres -c psql template1
    template1=# alter user postgres with encrypted password '<your superuser password>';
    template1=# <ctrl-d>

PostgreSQL runs under a separate user account called postgres.

  Set the password of the postgres user account to match the one of the
  superuser::

    $ sudo passwd -d postgres
    $ sudo su postgres -c passwd

  When prompted for the password, enter <your superuser password>.

Under Ubuntu, PostgreSQL uses Ident-based authentication by default. This means
that PostgreSQL requires that database users each have separate OS user
accounts. It's more convenient to separate the two, so that GMN can have a user
in PostgreSQL without also having to have an OS user account.

  Edit ``/etc/postgresql/8.4/main/pg_hba.conf``.

  Remove or comment out line::

    local   all         postgres                          ident

  Change::

    local   all         all                               ident

  To::

    local   all         all                               md5

  Restart PostgreSQL::

    $ sudo service postgresql-8.4 restart

  Create GMN user::

    $ sudo -u postgres createuser gmn
    postgres@ubuntu:~$
    Shall the new role be a superuser? (y/n) n
    Shall the new role be allowed to create databases? (y/n) n
    Shall the new role be allowed to create more new roles? (y/n) n
    Password: <your superuser password>

  Create a database for GMN::

    $ sudo -u postgres createdb -E UTF8 gmn
    Password: <your superuser password>

  Set the password for the GMN user::

    $ sudo -u postgres psql template1
    ALTER USER gmn WITH ENCRYPTED password '<your gmn user password>';

  In a later step, you will configure GMN with <your gmn user password>.
