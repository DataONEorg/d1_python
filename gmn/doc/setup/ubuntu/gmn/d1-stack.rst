Install the GMN software stack
==============================

Run the following commands to:

* Install the GMN software stack from PyPI into a Python virtual environment
* Install standard ``.bashrc`` for the ``gmn`` user

.. _clip1:

::

  sudo -Hu gmn bash -c '
    python3 -m venv /var/local/dataone/gmn_venv_py3
    . /var/local/dataone/gmn_venv_py3/bin/activate
    GMN_PKG_DIR=`python -c "import site; print(site.getsitepackages()[0])"`
    pip install --upgrade pip virtualenv
    pip install dataone.gmn
    cp ${GMN_PKG_DIR}/d1_gmn/deployment/bashrc ~/.bashrc
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip1">Copy</button>
..
