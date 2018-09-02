Update OS and install APT dependencies
======================================

Run the following commands to:

* Upgrade all installed packages to latest versions
* Install APT packaged GMN dependencies
* Set server clock to UTC timezone
* Open for HTTPS in the firewall

.. _clip1:

::

  sudo -H bash -c '
    apt update --yes
    apt dist-upgrade --yes
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip1">Copy</button>
..

Reboot if necessary.

.. _clip2:

::

  sudo -H bash -c '
    apt install --yes build-essential libssl-dev libxml2-dev libxslt1-dev \
    libffi-dev postgresql openssl curl python-pip python3-venv \
    python3-dev apache2 libapache2-mod-wsgi-py3 acl
  
    pip install --upgrade pip virtualenv

    timedatectl set-timezone Etc/UTC
    ufw allow 443
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip2">Copy</button>
..
