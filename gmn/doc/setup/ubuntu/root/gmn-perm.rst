Create ``gmn`` Account and Configure Permissions
================================================

Run the following commands to:

* Create the ``gmn`` user account (with password login disabled)
* Prepare the DataONE root directory
* Add or update permissions allowing the ``gmn`` user to
* Create and edit Apache configuration files

  * Restart the Apache and Postgres services
  * Read Apache and Postgres logs

.. note:: These commands can safely be run multiple times. Any missing permissions will be restored. Existing permissions will not be duplicated.

.. _clip1:

::

  sudo -H bash -c '
    # Create the gmn user account with password login disabled
    id -u gmn 1>/dev/null 2>&1 || adduser --ingroup www-data \
      --gecos "DataONE Generic Member Node" --disabled-password gmn

    ERR=$(sudo -u postgres createuser gmn 2>&1)
    [[ ${ERR} =~ "already exists" ]] || echo ${ERR}
    ERR=$(sudo -u postgres createdb -E UTF8 gmn3 2>&1)
    [[ ${ERR} =~ "already exists" ]] || echo ${ERR}

    mkdir -p /var/local/dataone
    chown -R gmn:www-data /var/local/dataone
    chmod -R 00755 /var/local/dataone

    # Allow the gmn user to create and edit Apache configuration files
    setfacl -Rm gmn:rwx /etc/apache2 /var/lib/apache2/site/enabled_by_admin/

    # Allow the gmn user to start and stop the Apache and Postgres services
    for s in postgresql apache2; do
      grep -q $s /etc/sudoers \
        || echo "gmn ALL=NOPASSWD:/etc/init.d/$s" >> /etc/sudoers
    done

    # Allow the gmn user to read existing Postgres and Apache logs
    setfacl -Rm gmn:rx /var/log/postgresql /var/log/apache2

    # Allow the gmn user to read future Postgres and Apache logs
    P="/etc/logrotate.d/gmn"
    echo  >$P "postrotate"
    echo >>$P "  setfacl -Rm gmn:rx /var/log/postgresql /var/log/apache2"
    echo >>$P "endscript"
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip1">Copy</button>
..
