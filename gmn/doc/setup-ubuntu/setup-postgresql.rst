Install and configure PostgreSQL
================================

This section describes how to set up PostgreSQL for GMN.

In PostgreSQL, the user with unlimited access is called the superuser. The superuser does not have a password by default.

The default peer authentication is used for the superuser and GMN users.

Install the PostgreSQL server and client:

  .. _clip1:

  ::

      [ `whoami` != root ] && sudo -Hs

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip1">Copy</button>
  ..

  .. _clip2:

  ::

    apt install --yes postgresql
    passwd -d postgres
    su postgres -c passwd

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip2">Copy</button>
  ..

  When prompted for the password, enter a new superuser password (and remember it :-).

  .. _clip3:

  ::

    su postgres -c 'createuser gmn'
    su postgres -c 'createdb -E UTF8 gmn2'

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip3">Copy</button>
  ..

