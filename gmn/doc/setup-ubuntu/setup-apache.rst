Install and configure Apache
============================

Run the commands below to:

  * Install Apache and required modules
  * Install default configuration for GMN in Apache
  * Set correct ServerName in GMN VirtualHost file
  * Install mod_wsgi from PyPI
    * We avoid the packaged version of mod_wsgi because it may not be binary compatible

  .. _clip1:

  ::

      [ `whoami` != root ] && sudo -Hs

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip1">Copy</button>
  ..

  .. _clip2:

  ::

    . /var/local/dataone/gmn_venv_py3/bin/activate
    export GMN_PKG_DIR=`python -c "import site; print(site.getsitepackages()[0])"`
    apt install --yes apache2 apache2-dev

    cp ${GMN_PKG_DIR}/d1_gmn/deployment/gmn3-ssl.conf /etc/apache2/sites-available
    cp ${GMN_PKG_DIR}/d1_gmn/deployment/forward_http_to_https.conf /etc/apache2/conf-available
    sed -Ei "s/(ServerName\s*).*/\1`hostname`/" /etc/apache2/sites-available/gmn3-ssl.conf

    a2enmod --quiet wsgi ssl rewrite
    a2enconf --quiet forward_http_to_https
    a2ensite --quiet gmn3-ssl

  .. raw:: html

    <button class="btn" data-clipboard-target="#clip2">Copy</button>
  ..
