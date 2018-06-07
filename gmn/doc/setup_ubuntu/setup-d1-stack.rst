Install the GMN software stack
==============================

GMN user account
~~~~~~~~~~~~~~~~

A user account named "gmn" is created. It will be set up to own the virtual environment and files that belong to GMN. It will also be used for authentication.

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

    $ sudo apt update --yes; sudo apt dist-upgrade --yes

  Reboot if necessary.

The GMN stack contains binary components that are built automatically during the install. This sets up the build environment and other dependencies that are distributed as software packages from Ubuntu's repositories.

  Set up packages::

    $ sudo apt install --yes build-essential python-dev libssl-dev libxml2-dev \
    libxslt1-dev libffi-dev postgresql-server-dev-10 openssl curl python-pip

  Install the GMN software stack from PyPI into a Python virtual environment::

    $ sudo --set-home pip install --upgrade pip virtualenv
    $ sudo mkdir -p /var/local/dataone/
    $ sudo chown gmn:www-data /var/local/dataone/

    $ sudo su gmn
    $ cd /var/local/dataone/
    $ virtualenv gmn_venv
    $ . ./gmn_venv/bin/activate
    $ pip install dataone.gmn


Shell environment
~~~~~~~~~~~~~~~~~

The gmn distribution includes a `.bashrc` file that contains various convenient settings and aliases for the `gmn` user. Installing the `.bashrc` file is optional but recommended. To install:

  $ cp /var/local/dataone/gmn_venv/lib/python2.7/site-packages/d1_gmn/deployment/bashrc ~/.bashrc

To activate the new environment:

  $ . ~/.bashrc

A brief message outlining the settings and aliases will be displayed on each login.
