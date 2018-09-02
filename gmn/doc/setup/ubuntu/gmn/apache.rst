Install and configure Apache
============================

Run the commands below to:

* Install default GMN configuration for Apache
* Set correct ServerName in GMN VirtualHost file

.. _clip2:

::

  sudo -Hu gmn bash -c '
    . /var/local/dataone/gmn_venv_py3/bin/activate
    GMN_PKG_DIR=`python -c "import site; print(site.getsitepackages()[0])"`
    FQDN=`python -c "import socket; print(socket.getfqdn())"`
    CONF_PATH=/etc/apache2/sites-available/gmn3-ssl.conf
    DELIMITER=`printf "#%.0s" {1..100}`

    cp ${GMN_PKG_DIR}/d1_gmn/deployment/gmn3-ssl.conf ${CONF_PATH}

    sed -Ei "s/www\.example\.com/${FQDN}/" ${CONF_PATH}

    a2enmod wsgi ssl alias
    a2enconf forward_http_to_https
    a2dissite 000-default
    a2ensite gmn3-ssl

    printf "%s\nUsing FQDN: %s\nIf this is incorrect, correct it in %s\n%s\n" \
     ${DELIMITER} ${FQDN} ${CONF_PATH} ${DELIMITER}
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip2">Copy</button>
..
