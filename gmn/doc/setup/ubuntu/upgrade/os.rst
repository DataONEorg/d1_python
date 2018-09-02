Upgrade Ubuntu 14.04 or 16.04 to 18.04
======================================

OS Upgrade
~~~~~~~~~~

Ubuntu 16.04 LTS can be upgraded directly to 18.04 LTS with ``do-release-upgrade``. 14.04 LTS must first be upgraded to 16.04 LTS, which means that the following procedure must be performed twice.

The ``dist-upgrade`` steps may seem redundant, but ``do-release-upgrade`` is more likely to complete successfully when the system is on the latest available kernel and packages.

.. _clip1:

::

  sudo -H bash -c '
    apt dist-upgrade
    apt autoremove
    reboot
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip1">Copy</button>
..

.. _clip2:

::

  sudo -H bash -c '
    do-release-upgrade
    reboot
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip2">Copy</button>
..

.. _clip3:

::

  sudo -H bash -c '
    apt dist-upgrade
    apt autoremove
    reboot
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip3">Copy</button>
..


Postgres Upgrade
~~~~~~~~~~~~~~~~

====== ========
Ubuntu Postgres
====== ========
14.04  9.3
16.04  9.5
18.04  10
====== ========

As the table shows, upgrading from Ubuntu 14.04 or 16.04 to 18.04 causes Postgres to be upgraded from major verson 9 to 10. The database storage formats are not compatible between major versions of Postgres, so the databases must be migrated from the old to the new version of Postgres.

The Ubuntu 18.04 upgrade process will install Postgres 10 side by side with Postgres 9.x. The ``pg_upgradecluster`` migration script is installed as well. However, the migration itself is not performed.

Run the commands below in order to migrate the databases over to Postgres 10 and remove the old database services.

If upgrading from Ubuntu 14.04, replace `9.5` with `9.3`. It is not necessary to perform a database migration after upgrading to 16.04.


.. _clip4:

::

  sudo -H bash -c '
    pg_dropcluster --stop 10 main
    pg_upgradecluster 9.5 main
    apt remove postgresql-9.5*
    reboot
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip4">Copy</button>
..
