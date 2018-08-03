GMN and DataONE background information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The GMN stack contains binary components that are built automatically during the install. This sets up the build environment and other dependencies that are distributed as software packages from Ubuntu's repositories.

GMN is distributed via `PyPI`_, the Python Package Index.

.. _PyPi: http://pypi.python.org

A user account named "gmn" is created. It will be set up to own the virtual environment and files that belong to GMN. It will also be used for authentication.

The gmn distribution includes a `.bashrc` file that contains various convenient settings and aliases for the `gmn` user. Installing the `.bashrc` file is optional but highly recommended, as it provides a standardized environment for administrators.

A brief message outlining the available settings and aliases will be displayed on each login.


Setting up Apache.

The :term:`mod_ssl` module handles TLS/SSL connections for GMN and validates client side certificates. It is included in the apache2-common package, installed in the next step.

The :term:`mod_wsgi` module enables Apache to communicate with :term:`Django` and GMN.


Asynchronous processing
~~~~~~~~~~~~~~~~~~~~~~~

CNs may send various messages to MNs. These include replication requests and System Metadata update notifications. Such requests are queued by GMN and handled asynchronously.

The asynchronous processes are implemented as Django management commands that are launched at regular intervals by :term:`cron`. The management commands examine the queues and process the requests.

The asynchronous processes connect to CNs and other MNs on behalf of your GMN instance. These connections are made over TLS/SSL and use the client side certificate stored in ``/var/local/dataone/certs/client``.

~~~~~~~~~~~~~~~~

TODO

The CLI is distributed via PyPI, the Python Package Index.

  Set up OS packages required by some of the CLI's PyPI distributed
  dependencies. This includes a build environment for DataONE Python extensions.

~~~

