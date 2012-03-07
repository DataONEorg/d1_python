GMN Asynchronous Processes
==========================

GMN uses asynchronous processes, launched by :term:`cron` to perform various
tasks that are not directly related to servicing client requests, such as
replication and object store pruning.

**<This section is unfinished>**

Brief overview of the tasks that must be performed:

* Configure cron to launch the processes at appropriate intervals

* Set the permissions and environment of the processes

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
