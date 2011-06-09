Step 2: Apache
==============

Apache setup.


==================== ==============================================
Component            Minimum Version
==================== ==============================================
Apache               2
apache2              \
libapache2-mod-wsgi  \
apache2-threaded-dev \
openssh-server       \
==================== ==============================================

viewing files:

openssl rsa -noout -text -in server.key
openssl req -noout -text -in server.csr
openssl rsa -noout -text -in ca.key
openssl x509 -noout -text -in ca.crt



Install Apache2 packages::

  $ sudo apt-get install apache2 apache2 apache2-threaded-dev 

  \
   


Apache
``````

GMN has been tested with Apache 2.2.

These instructions have been tested on Ubuntu 10.04 LTS. Adjust the paths to
match your configuration.


* Set up GMN in a new or existing VirtualHost section. An example site file
  is included below. It is a modified version of the default site file at::

    /etc/apache2/sites-available/default

  Note that the settings for AllowEncodedSlashes and AcceptPathInfo that are
  included at the top of the VirtualHost section are required for GMN to
  function properly. Also see `Apache Configuration for DataONE Services`_ for
  other important information about these settings.

* Restart Apache::

    apache2ctl restart


.. _`Apache Configuration for DataONE Services`:
  http://mule1.dataone.org/ArchitectureDocs-current/notes/ApacheConfiguration.html#configuration


:doc:`setup-mod-wsgi`

