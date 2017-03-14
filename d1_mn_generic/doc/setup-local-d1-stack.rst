Install the GMN software stack
==============================

GMN user account
~~~~~~~~~~~~~~~~

A user account named "gmn" is created. It will be set up to own the virtual
environment and files that belong to GMN. It will also be used for
authentication.

  Create the gmn user account::

    $ sudo adduser --ingroup www-data gmn

  Follow the prompts. The fields can be left blank or used for brief
  descriptions. For instance, ``Full Name``, can be set to ``Owner of the
  DataONE Generic Member Node virtual environment``.


GMN software stack
~~~~~~~~~~~~~~~~~~

GMN is distributed via `PyPI`_, the Python Package Index.

.. _PyPi: http://pypi.python.org

  Make sure the system is up to date::

    $ sudo apt-get --yes update; sudo apt-get --yes dist-upgrade

  Reboot if necessary.

The GMN stack contains binary components that are built automatically during
the install. This sets up the build environment and other dependencies that
are distributed as software packages from Ubuntu's repositories.

``postgresql-server-dev-*`` is used when building the Psycopg2 PostgreSQL
database adapter for Python. ``libssl-dev`` is used when building the DataONE
certificate extensions. ``libxml2-dev`` and ``libxslt1-dev`` are dependencies of
the Foresite Toolkit, which handles parsing of OAI-ORE Resource Maps.

  Set up packages::

    $ sudo apt-get --yes install build-essential python-dev libssl-dev libxml2-dev \
    libxslt1-dev libffi-dev postgresql-server-dev-9.5 openssl curl

    $ sudo apt-get --yes install build-essential python-dev libssl-dev libxml2-dev \
    libxslt1-dev libffi-dev postgresql-server-dev-9.3 openssl curl

  Install the GMN software stack from PyPI into a Python virtual environment::

    $ sudo apt-get --yes install python-pip; \
    sudo pip install --upgrade pip; \
    sudo pip install virtualenv; \
    sudo mkdir -p /var/local/dataone/{gmn_venv,gmn_object_store}; \
    cd /var/local/dataone; \
    sudo chown gmn:www-data gmn_venv; \
    sudo su gmn

    $ virtualenv gmn_venv; \
    . ./gmn_venv/bin/activate; \
    pip install --upgrade setuptools==33.1.1; \
    pip install cachecontrol==0.11.7; \
    pip install dataone.gmn

    $ exit


  Use the GMN Python virtual environment by default for the gmn user::

    $ sudo nano /home/gmn/.bashrc

  Close to the top, just after the section that aborts if not running
  interactively, add::

    PATH=/var/local/dataone/gmn_venv/bin/:$PATH
