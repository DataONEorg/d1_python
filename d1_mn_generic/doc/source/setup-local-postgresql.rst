Install and configure PostgreSQL
================================

This section describes how to set up PostgreSQL for GMN.

In PostgreSQL, the user with unlimited access is called the superuser. The
superuser does not have a password by default.

The default peer authentication is used for the superuser and GMN users.

  Install the PostgreSQL server and client::

    $ sudo apt-get install postgresql

  Set the password of the postgres user account to match the one of the
  superuser::

    $ sudo passwd -d postgres
    $ sudo su postgres -c passwd

  When prompted for the password, enter <your superuser password>.

  Create GMN user::

    $ sudo -u postgres createuser gmn

  Create a database for GMN::

    $ sudo -u postgres createdb -E UTF8 gmn
