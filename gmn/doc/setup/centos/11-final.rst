Final configuration and startup
===============================

Filesystem permissions
~~~~~~~~~~~~~~~~~~~~~~

  Set all the files to be owned by the gmn account, and to be writable by www-data::

    $ sudo chown -R gmn:apache /var/local/dataone
    $ sudo chmod -R g+w /var/local/dataone/

Initialize the database
~~~~~~~~~~~~~~~~~~~~~~~

  ::

    sudo -Hu gmn bash -c '
      cd /var/local/dataone
      source gmn_venv_py3/bin/activate
      python /var/local/dataone/gmn_venv_py3/lib/python3.6/site-packages/d1_gmn/manage.py migrate --run-syncdb
    '

Set server to UTC timezone (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GMN translates incoming date-times to UTC and provides outgoing date-times in UTC. Because of this, it is convenient to run the server in UTC, so that server related timestamps, such as the ones in logs, match up with timestamps stored in the GMN database and provided in DataONE REST API responses.

To check your time format::

  $ date

The output should specify that that time given is in UTC, for example:
::

  [mySudoerUser@centos7 dataone]$ date
    Thu Mar 23 20:27:52 UTC 2017

If not in UTC time, try::

  $ rm -f /etc/localtime; ln -s /usr/share/zoneinfo/UTC /etc/localtime
  $ echo 'ZONE="UTC"' > /etc/sysconfig/clock

Starting GMN
~~~~~~~~~~~~

GMN should now be ready to start. Simply restart Apache::

  $ sudo service httpd restart

Check the Apache logs for error messages. In case of any issues, refer to
:doc:`../troubleshooting`

Continue to the next section to test your new node.
