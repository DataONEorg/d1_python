GMN v2 migration
================

This section describes how to migrate to GMN v2 from an existing, operational
instance of GMN v1. If you are working on a fresh install, start on :setup-local:.

* Prepare dependencies

    $ sudo pip install --upgrade pip virtualenv
    $ sudo apt-get install libffi-dev

* Become the gmn user

    $ sudo su gmn

* Create and activate virtual environment for GMN v2

    $ cd /var/local/dataone
    $ virtualenv --distribute gmn_venv
    $ . gmn_venv/bin/activate

* Install GMN v2 from PyPI

    $ pip install dataone.gmn==2.0.0

* Configure GMN v2 instance and migrate settings from GMN v1

    $ sudo /var/local/dataone/gmn_venv/lib/python2.7/site-packages/gmn/deployment/migrate_v1_to_v2.sh

* Migrate contents from GMN v1

    $ /var/local/dataone/gmn_venv/bin/python /var/local/dataone/gmn_venv/lib/python2.7/site-packages/gmn/manage.py migrate_v1_to_v2

* Adjust settings in /etc/apache2/sites-available/gmn2-ssl.conf

  * Set `ServerName` to the fully qualified domain name (FQDN) of your node.

  * If the node is registered in a DataONE environment, uncomment `SSLCACertificateFile`.

  * Adjust certificate paths if required.

  * Restart Apache with `sudo service apache2 restart`.
