Configure the GMN asynchronous processes
========================================

CNs may send various messages to MNs. These include replication requests and
System Metadata update notifications. Such requests are queued by GMN and
handled asynchronously.

The asynchronous processes are implemented as Django management commands that
are launched at regular intervals by :term:`cron`. The management commands
examine the queues and process the requests.

The asynchronous processes connect to CNs and other MNs on behalf of your GMN
instance. These connections are made over TLS/SSL and use the client side
certificate stored in ``/var/local/dataone/certs/client``.


Set up cron jobs
~~~~~~~~~~~~~~~~

  Edit the cron table for the gmn user::

    $ sudo crontab -e -u gmn

  Add::

    # Process the replication queue.
    * * * * * cd /var/local/dataone/gmn/lib/python2.7/site-packages/service && /var/local/dataone/gmn/bin/python ./manage.py process_replication_queue >>gmn_replication.log 2>&1
    # Process the System Metadata refresh queue.
    * * * * * cd /var/local/dataone/gmn/lib/python2.7/site-packages/service && /var/local/dataone/gmn/bin/python ./manage.py process_system_metadata_refresh_queue >>gmn_sysmeta.log 2>&1

  This sets the processes to run every minute. To alter the schedule, consult
  the crontab manual::

    $ man 5 crontab
