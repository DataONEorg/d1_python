Install the GMN software stack
==============================

GMN user account
~~~~~~~~~~~~~~~~

A user account named "gmn" is created. It will be set up to own the files that
belong to GMN. It will also be used for authentication.

  Create the gmn user account::

    $ sudo adduser --ingroup www-data gmn

  Follow the prompts.


GMN software stack
~~~~~~~~~~~~~~~~~~

GMN is distributed via PyPI, the Python Package Index.

  Set up server packages:

  * The build environment for DataONE Python extensions and lxml
  * Commands used in the install

  ::

    $ sudo apt-get install build-essential python-dev libssl-dev libxml2-dev \
    libxslt-dev postgresql-server-dev-8.4 openssl curl

  Install the GMN software stack from PyPI, into a Python virtual environment::

    $ sudo apt-get install python-pip
    $ sudo pip install pip --upgrade
    $ sudo pip install virtualenv
    $ sudo mkdir -p /var/local/dataone/gmn
    $ cd /var/local/dataone
    $ sudo chown gmn:www-data gmn
    $ su gmn
    $ virtualenv --distribute gmn
    $ cd gmn
    $ . bin/activate
    $ pip install dataone.generic_member_node
    $ <ctrl-d>

  Use the GMN Python virtual environment by default for the gmn user::

    $ sudo pico /home/gmn/.bashrc

  * Close to the top, just after the line that aborts if not running
    interactively, add::

      PATH=/var/local/dataone/gmn/:$PATH
