Configure the GMN asynchronous processes
========================================

CNs may send various messages to MNs. These include replication requests and
System Metadata update notifications. Such requests are queued by GMN and
handled asynchronously.

The asynchronous processes are implemented as Django management commands that
are launched at regular intervals by :term:`cron`. The management commands
examine the queues and process the requests.

Security
~~~~~~~~

The asynchronous processes connect to CNs and other MNs on behalf of your GMN
instance. Also, they connect directly to your GMN instance. All of these
connections are made over TLS/SSL and use the client side certificate that was
issued to you by DataONE in the registration process. GMN recognizes this
certificate and gives such connections access to internal APIs.


Set up cron jobs
~~~~~~~~~~~~~~~~

  Edit the cron table for the gmn user::

    $ su gmn
    $ crontab -e

  Add::

    # Process the replication queue.
    * * * * * cd /var/local/dataone/gmn/lib/python2.6/site-packages/service && /var/local/dataone/gmn/bin/python ./manage.py process_replication_queue >>gmn_replication.log 2>&1
    # Process the System Metadata dirty queue.
    * * * * * cd /var/local/dataone/gmn/lib/python2.6/site-packages/service && /var/local/dataone/gmn/bin/python ./manage.py process_system_metadata_dirty_queue >>gmn_sysmeta.log 2>&1

  This sets the processes to run every minute. To alter the schedule, consult
  the crontab manual::

    $ man 5 crontab
