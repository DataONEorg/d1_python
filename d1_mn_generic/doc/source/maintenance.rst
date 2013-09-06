Maintenance
===========

Notes on maintaining a GMN instance.


GMN software stack upgrade
~~~~~~~~~~~~~~~~~~~~~~~~~~

Upgrading the GMN software stack to the latest release.

::

  $ cd /var/local/dataone; su gmn;

* Type the password for the gmn user when prompted.

::

  virtualenv --distribute gmn; cd gmn; . bin/activate; \
  pip install --upgrade dataone.generic_member_node
  $ <ctrl-d>
