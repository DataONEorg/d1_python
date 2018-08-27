Install the GMN software stack
==============================

Run the following commands to:

  * Upgrade all installed packages to latest version
  * Create the GMN user account
  * Install packaged dependencies for the DatONE stack
  * Install the GMN software stack from PyPI into a Python virtual environment

  .. _clip1:

  ::

    sudo apt update --yes; sudo apt dist-upgrade --yes

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip1">Copy</button>
  ..

  Reboot if necessary.


  .. _clip2:

  ::

    sudo adduser --ingroup www-data --gecos "DataONE Generic Member Node" gmn

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip2">Copy</button>
  ..

  Type a password for the GMN user when prompted.

  .. _clip3:

  ::

    [ `whoami` != root ] && sudo -Hs

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip3">Copy</button>
  ..

  .. _clip4:

  ::

    apt install --yes build-essential libssl-dev libxml2-dev libxslt1-dev \
    libffi-dev postgresql-server-dev-10 openssl curl python-pip python3-venv \
    python3-dev libapache2-mod-wsgi-py3
    pip install --upgrade pip virtualenv
    mkdir -p /var/local/dataone/
    python3 -m venv /var/local/dataone/gmn_venv_py3
    . /var/local/dataone/gmn_venv_py3/bin/activate
    pip install --upgrade pip
    pip install dataone.gmn
    chown -R gmn:www-data /var/local/dataone
    cp `python -c "import site; print(site.getsitepackages()[0])"`\
    /d1_gmn/deployment/bashrc /home/gmn/.bashrc

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip4">Copy</button>
  ..
