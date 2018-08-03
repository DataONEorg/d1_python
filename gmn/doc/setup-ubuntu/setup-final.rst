Final configuration and startup
===============================

GMN translates incoming date-times to UTC and provides outgoing date-times in UTC. Because of this, it is convenient to run the server in UTC, so that server related timestamps, such as the ones in logs, match up with timestamps stored in the GMN database and provided in DataONE REST API responses.

Performs steps:

  * Set all the files to be owned by the GMN account, and to be writable by www-data
  * Set server to UTC timezone
  * Open for HTTPS in the firewall
  * Initialize the GMN database

  .. _clip1:

  ::

      [ `whoami` != root ] && sudo -Hs

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip1">Copy</button>
  ..

  .. _clip2:

  ::

    chown -R gmn:www-data /var/local/dataone/
    chmod -R g+w /var/local/dataone/
    timedatectl set-timezone Etc/UTC
    ufw allow 443

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip2">Copy</button>
  ..

  .. _clip3:

  ::

      [ `whoami` != gmn ] && sudo -Hsu gmn

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip3">Copy</button>
  ..

  .. _clip4:

  ::

    . /var/local/dataone/gmn_venv/bin/activate
    export GMN_PKG_DIR=`python -c "import site; print(site.getsitepackages()[0])"`
    python ${GMN_PKG_DIR}/d1_gmn/manage.py migrate --run-syncdb

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip4">Copy</button>
  ..


Starting GMN
~~~~~~~~~~~~

GMN should now be ready to start. Simply restart Apache:

  .. _clip5:

  ::

    sudo service apache2 restart

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip5">Copy</button>
  ..


Check the Apache logs for error messages. In case of any issues, refer to :doc:`../troubleshooting`

Continue to the next section to test your new node.
