GMN Setup Background Information
================================

PyPI
~~~~

GMN is distributed via `PyPI`_, the Python Package Index.

.. _PyPi: http://pypi.python.org

bashrc
~~~~~~

The gmn distribution includes a `.bashrc` file that contains various convenient settings and aliases for the `gmn` user. Installing the `.bashrc` file is optional but highly recommended, as it provides a standardized environment for administrators.

A brief message outlining the available settings and aliases will be displayed on each login.


Apache
~~~~~~

The :term:`mod_ssl` module handles TLS/SSL connections for GMN and validates client side certificates. It is included in the apache2-common package.

The :term:`mod_wsgi` module enables Apache to communicate with :term:`Django` and GMN.


Postgres
~~~~~~~~~~

GMN uses Postgres Peer authentication, which is default in Ubuntu.

With Peer authentication, a process belonging to a given user can access Postgres as long as a corresponding username has been set up in Postgres with the ``createuser`` command.

As part of the GMN install, an empty database is created in Postgres with the ``createdb`` command. This database is owned by the ``postgres`` user and Peer authenticated users have permission to create tables in it.

GMN is configured to use this database via the ``DATABASES/NAME`` setting in ``settings.py``. Before starting GMN, a Django management command that creates the tables that are required by GMN is run as the ``gmn`` user, which causes the ``gmn`` user to become the owner of the tables.


Asynchronous processing
~~~~~~~~~~~~~~~~~~~~~~~

CNs may send various messages to MNs. These include replication requests and System Metadata update notifications. Such requests are queued by GMN and handled asynchronously.

The asynchronous processes are implemented as Django management commands that are launched at regular intervals by :term:`cron`. The management commands examine the queues and process the requests.

The asynchronous processes connect to CNs and other MNs on behalf of your GMN instance. These connections are made over TLS/SSL and use the client side certificate stored in ``/var/local/dataone/certs/client``.


Authentication and authorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:doc:`Authentication and authorization </gmn/use-authn-and-authz>` in DataONE is based on :term:`X.509` (SSL) certificates.

GMN authenticates to incoming connections from :term:`DataONE` :term:`client`\ s and other parts of the DataONE infrastructure, such as :term:`CN`\ s by providing a :term:`server side certificate` during the SSL/TLS handshake.

By default, a stand-alone instance of GMN uses a non-trusted, self-signed, "snakeoil" server side certificate. This defers the purchase of a publicly trusted certificate from a 3rd party :term:`CA` such as VeriSign or Thawte until the stand-alone instance is registered with DataONE.

A stand-alone instance that is not going to be registered with DataONE can use the non-trusted certificate indefinitely. Such a certificate is as secure as a publicly trusted certificate when used locally.

In addition to acting as servers in the DataONE infrastructure, Member Nodes also act as clients, initiating connections to other Nodes. When connecting to other Nodes, Member Nodes authenticate themselves in a process called
:term:`client side authentication`, in which a client side certificate is provided over an LTS/SSL connection.

Nodes that are registered with DataONE will only trust Member Node connections where a client side sertificate issued by the DataONE :term:`CA` is provided. However, a stand-alone instance of GMN will not connect to registered Member Nodes, so a non-trusted client side certificate can be used instead.



Misc
~~~~

GMN translates incoming date-times to UTC and provides outgoing date-times in UTC. Because of this, it is convenient to run the server in UTC, so that server related timestamps, such as the ones in logs, match up with timestamps stored in the GMN database and provided in DataONE REST API responses.

