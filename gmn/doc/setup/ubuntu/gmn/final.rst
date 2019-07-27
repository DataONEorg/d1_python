Final configuration and startup
===============================

Run the following commands to:

- Configure the GMN settings that are required for running a local instance of GMN.
- Initialize the GMN database

.. _clip1:

::

  sudo -Hu gmn bash -c '
    . /var/local/dataone/gmn_venv_py3/bin/activate
    GMN_PKG_DIR=`python -c "import site; print(site.getsitepackages()[0])"`
    FQDN=`python -c "import socket; print(socket.getfqdn())"`
    DELIMITER=`printf "#%.0s" {1..100}`
    SETTINGS_PATH=${GMN_PKG_DIR}/d1_gmn/settings.py
    cp ${GMN_PKG_DIR}/d1_gmn/settings_template.py ${SETTINGS_PATH}
    sed -Ei "s/MIDDLEWARE_CLASSES/MIDDLEWARE/" ${SETTINGS_PATH}
    sed -Ei "s/'"'"'gmn2'"'"'/'"'"'gmn3'"'"'/" ${SETTINGS_PATH}
    sed -Ei "s/(\s*)(.*my\.server\.name\.com.*)/\1'"'"'${FQDN}'"'"',/" ${SETTINGS_PATH}
    python ${GMN_PKG_DIR}/d1_gmn/manage.py migrate --run-syncdb
    printf "%s\nUsing FQDN: %s\nIf this is incorrect, correct it in %s\n%s\n" \
     ${DELIMITER} ${FQDN} ${SETTINGS_PATH} ${DELIMITER}
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip1">Copy</button>
..


Starting GMN
~~~~~~~~~~~~

GMN should now be ready to start. Simply restart Apache:

.. _clip2:

::

  sudo service apache2 restart

.. raw:: html

  <button class="btn" data-clipboard-target="#clip2">Copy</button>
..


Check the Apache logs for error messages. In case of any issues, refer to :doc:`/d1_gmn/troubleshooting/index`

Continue to the next section to test your new node.
