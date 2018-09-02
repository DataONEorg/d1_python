Hosting multiple Member Nodes from the same GMN instance
========================================================

A single GMN instance can host multiple separate MNs, referred to as "multi-hosting". The number of MNs hosted within a GMN instance is limited only by the available hardware.

In a multi-hosting setup, each MN is functionally equivalent to individual MNs hosted on separate servers. They are individually configured and have separate management commands. Each MN has its own database and Science Object storage area in the filesystem.

At the same time, by sharing a server and a Python virtual environment, any upgrades or other system maintenance automatically applies to all the MNs.

Overall, multi-hosting can significantly lower the time required to maintain the services, lower hardware costs, and lower the complexity of deployments.

A multi-hosting setup works by configuring Apache to alias separate MN BaseURLs to separate WSGI configuration files. Each WSGI file then invokes GMN using a separate settings file. In turn, each settings file specifies a different database, Science Object storage area, and log file.

As each MN has its own settings file, the MNs can be configured individually for such things as branding and replication policies.

In order to be able to specify which MN a management command applies to, separate management commands are set up as well.

As with MNs hosted on separate servers, each MN needs to have a unique BaseURL. If the BaseURLs use the same domain name, they can share a single server side certificate and DNS record. E.g.:

::

  https://xyz.node.edu/mn-one
  https://xyz.node.edu/mn-two
  
Each MN can also have completely unrelated BaseURLs, as long as all the domain names resolve to the same server. In such as setup, the server can be set up to issue separate server side certificates for each MN, or both MNs can issue a shared certificate that covers both domain names. E.g.:

::

  https://mn-one.some.domain.edu/mn/
  https://mn-two.another.domain.org/some/path/



Example
~~~~~~~

What follows is a complete example on how to add a second MN to a GMN instance that has already been set up as described in the standard setup procedure, and is currently exposing a single working MN. After adding the second MN, there will be no difference to the original MN as seen from the user side.

In this example, we'll just call the original MN, "a", and the new MN, "b". In a real setup, these names would be selected to reflect the actual MN names.

If the new MN is intended to be joined to a DataONE environment, start by obtaining a client side certificate for the MN from DataONE. If the MN will be used for local testing only, a self signed certificate can be generated as described in :doc:`ubuntu/gmn/authn-ca`. Make sure to modify the names of the output files if previously generated files are still in use. Then install the certificates as described in :doc:`ubuntu/gmn/authn-client`.

::

  $ cdgmn
  $ sudo service apache2 stop 

  $ mv wsgi.py wsgi_a.py
  $ mv settings.py settings_a.py
  $ mv manage.py manage_a.py
  
  $ cp wsgi_a.py wsgi_b.py
  $ cp settings_a.py settings_b.py
  $ cp manage_a.py manage_b.py

  $ editor wsgi_a.py
    * Edit: d1_gmn.settings -> d1_gmn.settings_a

  $ editor manage.py
    * Edit: d1_gmn.settings -> d1_gmn.settings_a

  $ editor wsgi_b.py
    * Edit: d1_gmn.settings -> d1_gmn.settings_b

  $ editor manage.py
    * Edit: d1_gmn.settings -> d1_gmn.settings_b

  $ editor settings_b.py
    * Edit the settings as if setting up a regular new MN on a separate server
    * In addition:
      * Change the following settings so that they’re different from the values
      * used by the original MN:
      * NODE_BASEURL, DATABASE.NAME, LOG_PATH, OBJECT_STORE_PATH
      * For this example, we’ll assume that we just added "_b" to the values

Create and initialize a database for the new MN:

::

  $ su postgres -c 'createdb -E UTF8 gmn2_b'
  $ ./manage_b.py migrate --run-syncdb

Configure Apache:

::

  $ sudo -e /etc/apache2/sites-enabled/gmn3-ssl.conf

Duplicate and modify `WSGIScriptAlias` and `WSGIDaemonProcess` as follows. This pattern is used when the MNs use the same domain main in the BaseURL. It leaves the original MN available under the same BaseURL as before, and exposes the new MN under /mn_b/.

::

  WSGIScriptAlias         /mn   ${gmn_root}/wsgi_a.py
  WSGIScriptAlias         /mn_b ${gmn_root}/wsgi_b.py
  WSGIDaemonProcess       gmn_a user=gmn processes=2 threads=25
  WSGIDaemonProcess       gmn_b user=gmn processes=2 threads=25

Add a new section to apply separate process groups to each MN (without this, both MNs will randomly be served from both BaseURLs):

::

  <Location /mn>
     WSGIProcessGroup gmn_a
     SSLOptions +ExportCertData
  </Location>
  <Location /mn_b>
     WSGIProcessGroup gmn_b
     SSLOptions +ExportCertData
  </Location>

Create crontab entries for the async jobs for the new MN:

::

  $ crontab -e

Duplicate the two crontab entries, then change the first two from `manage.py` to `manage_a.py` and the last two to `manage_b.py`. Similarly append `_a` and `_b` to the log filenames.

Then all that remains is to start Apache again to make the new MN available for use.

::

  $ sudo service apache2 start

Management commands for the original MN are now launched via `manage_a.py`, and via `manage_b.py` for the new MN. E.g., to register the new MN in a DataONE environment, use `manage_b.py node register`.

Depending on how backups are performed on the server, the new database and the Science Object storage area for the new MN may have to be added to the procedures.

Other administrative procedures, such as OS, GMN and DataONE Python stack upgrades, likely remain unchanged.
