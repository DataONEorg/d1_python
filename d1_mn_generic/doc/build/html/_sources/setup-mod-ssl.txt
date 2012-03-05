mod_ssl
=======

Setting up :term:`mod_ssl`.

\

==================== ==============================================
Component            Tested version(s)
==================== ==============================================
apache2.2-common     2.2.14-5ubuntu8.4
==================== ==============================================


The mod_ssl module is included in the apache2-common package.

  Install the apache2-common package::

    $ sudo apt-get install apache2.2-common

  Enable the module::

    $ sudo a2enmod ssl


:doc:`setup-authn-server`
