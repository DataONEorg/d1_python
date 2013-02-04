Configure the GMN Asynchronous Processes
========================================

.. Note:: It is only necessary to perform this step if GMN has been configured
  to run as a Tier 4 node. See :doc:`setup-tier`.

GMN stores replication requests, submitted by CNs, in a queue. An asynchronous
replication process, launched at regular intervals by :term:`cron`, connects to
GMN and process any queued replication requests.

This describes how to set the asynchronous processes up to run from their
default location. However, the processes can run from any location, including a
different server. Running the asynchronous processes on a different server *may*
be beneficial if the GMN server is very busy.

The asynchronous processes connect to CNs and other MNs on behalf of this GMN
instance and thus need access to the DataONE client side certificate (issued to
this GMN instance by DataONE in the registration process). As this GMN instance
already has been set up to accept connections from other DataONE signed
certificates, the async processes only need to be set up with a single
certificate.


Enable access to internal REST service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The asynchronous processes use REST interfaces internal to GMN to access and
update information they require in order to perform their tasks. Only the client
side certificate issued to this instance of GMN by DataONE should enable
connection to GMNs internal interfaces. Because of this, access to the internal
interfaces is protected by a whitelist of subjects.

  Configure GMN to allow the Subject DN in the certificate used by the
  asynchronous processes to access the GMN internal REST APIs.

  Edit: ``/var/local/dataone/gmn/lib/python2.6/site-packages/service/settings_site.py``

  * Add the DataONE compliant serialization of the DN to GMN_INTERNAL_SUBJECTS.
    E.g., `CN=MyMemberNode,O=DataONE,C=US,DC=dataone,DC=org`


Replication
~~~~~~~~~~~

  Create a cron entry for the replication process::

    $ su gmn
    $ crontab -e

  Add::

    * * * * * cd /var/local/dataone/gmn/lib/python2.6/site-packages/service/async && /var/local/dataone/gmn/bin/python ./process_replication_queue.py >>process_replication_queue.log 2>&1

  This sets the replication process to run every minute. To alter the schedule,
  consult the crontab manual::

    $ man 5 crontab
