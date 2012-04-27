GMN Asynchronous Processes
==========================

GMN uses asynchronous processes, launched at regular intervals by :term:`cron`,
to perform various tasks that are not directly related to servicing client
requests.

This describes how to set the asynchronous processes up to run from their
default location of `/var/local/dataone/mn_generic/service/async/`. However,
the processes can run from any location, including a different server. Running
the asynchronous processes on a different server may be beneficial if the GMN
server is very busy.


Certificate setup
~~~~~~~~~~~~~~~~~

The asynchronous processes authenticate themselves to GMN by connecting via
TLS/SSL and providing a certificate. The instructions below use the certificate
that was provided by DataONE when the MN was registered. This is convenient
because the certificate is signed by the DataONE CA, which MNs are required to
trust.

  Create copies of the DataONE provided certificate and private key. Store the
  copies in the following location::

    /var/local/dataone/mn_generic/service/async/

  As an alternative, the `--cert-path` and `--key-path` command line options,
  supported by all the asynchronous processes, can be set to the absolute paths
  to the certificates in a different location.


Enable access to internal REST service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The asynchronous processes use REST services internal to GMN to access and
update information they require in order to perform their tasks. GMN allows
only connections made under specific Subject DNs to access these interfaces.

  Configure GMN to allow the Subject DN in the certificate used by the
  asynchronous processes to access the GMN internal REST APIs.

  Edit: ``/var/local/dataone/mn_generic/service/settings_site.py``

  *



Replication
~~~~~~~~~~~

The GMN service stores replication requests in a queue. The asynchronous
replication process uses



  Create a cron entry for the replication process::

    $ crontab -e

  Add::

    * * * * * cd /var/local/dataone/mn_generic/service/async && ./process_replication_queue.py --cert-path <cert filename> --key-path <key filename>  >>process_replication_queue.log 2>&1

  This sets the replication process to run every minute. To alter the schedule,
  consult the crontab manual::

    $ man 5 crontab


Brief overview of the processes that must be performed:

* If the processes are not running locally (on the same machine as GMN), they
  must authenticate themselves to GMN. Alternatives:

  * Get a long term certificate from CILogon (via their regular portal, not the
    DataONE portal). Since GMN is already set up to trust certificates from
    CILogon, all that then remains is to set GMN up to trust the subject in the
    certificate that was obtained from CILogon.

  * Create a local CA, set GMN up to trust this CA and sign certificates for the
    processes with this CA.

  * Other security schemes may be sufficient, based on the environment in which
    GMN is set up, such as allowing the processes to connect without
    authentication from a local LAN or specific IP address


:doc:`setup-whitelist`
