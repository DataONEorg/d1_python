Basic Configuration
===================

Configure the GMN settings that are required for running a local instance of GMN.

  Create a copy of the GMN site settings template::

    $ cd /var/local/dataone/gmn_venv/lib/python2.7/site-packages/gmn
    $ sudo cp settings_site_template.py settings_site.py

Django requires a unique, secret key to be set up for each application.

  Set a random secret key in ``settings_site.py``::

    $ sudo sed -i 's/^SECRET_KEY.*/SECRET_KEY = '\'`sudo openssl rand -hex 32`\''/' settings_site.py

