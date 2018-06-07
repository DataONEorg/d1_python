Configure the GMN asynchronous processes
========================================

CNs may send various messages to MNs. These include replication requests and System Metadata update notifications. Such requests are queued by GMN and handled asynchronously.

The asynchronous processes are implemented as Django management commands that are launched at regular intervals by :term:`cron`. The management commands examine the queues and process the requests.

The asynchronous processes connect to CNs and other MNs on behalf of your GMN instance. These connections are made over TLS/SSL and use the client side certificate stored in ``/var/local/dataone/certs/client``.


Set up cron jobs
~~~~~~~~~~~~~~~~

  Edit the cron table for the gmn user::

    $ sudo crontab -e -u gmn

  Add::

    GMN_ROOT = /var/local/dataone/gmn_venv
    SERVICE_ROOT = /var/local/dataone/gmn_venv/lib/python2.7/site-packages/d1_gmn
    PYTHON_BIN = /var/local/dataone/gmn_venv/bin/python

    # Process the Science Object replication queue
    * * * * * sleep $(expr $RANDOM \% $(30 * 60)) ; $PYTHON_BIN $SERVICE_ROOT/manage.py process_replication_queue >> $SERVICE_ROOT/gmn_replication.log 1>&1
    # Process the System Metadata refresh queue
    * * * * * sleep $(expr $RANDOM \% $(30 * 60)) ; $PYTHON_BIN $SERVICE_ROOT/manage.py process_refresh_queue >> $SERVICE_ROOT/gmn_sysmeta.log 2>&1

  This sets the processes to run once every hour, with a random delay that distributes network traffic and CN load over time. To alter the schedule, consult
  the crontab manual::

    $ man 5 crontab

