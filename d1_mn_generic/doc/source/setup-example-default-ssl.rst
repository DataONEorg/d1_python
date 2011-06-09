.. _default-ssl-example:

Example ``default-ssl`` Apache configuration file
-------------------------------------------------

This configuration file was taken from a working GMN installation.

::

  <VirtualHost *:80>
    AllowEncodedSlashes On
    AcceptPathInfo On

    ServerAdmin dahl@unm.edu

    DocumentRoot /var/www

    <Directory />
      Options FollowSymLinks
      AllowOverride None
    </Directory>

    <Directory /var/www/>
      Options Indexes FollowSymLinks MultiViews
      AllowOverride None
      Order allow,deny
      allow from all
    </Directory>

    ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
    <Directory "/usr/lib/cgi-bin">
      AllowOverride None
      Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
      Order allow,deny
      Allow from all
    </Directory>

    ErrorLog /var/log/apache2/error.log

    # Possible values include: debug, info, notice, warn, error, crit,
    # alert, emerg.
    LogLevel debug

    CustomLog /var/log/apache2/access.log combined

      Alias /doc/ "/usr/share/doc/"
      <Directory "/usr/share/doc/">
          Options Indexes MultiViews FollowSymLinks
          AllowOverride None
          Order deny,allow
          Deny from all
          Allow from 127.0.0.0/255.0.0.0 ::1/128
      </Directory>

    # Generic Member Node (GMN)

    WSGIScriptAlias /mn /var/local/mn/mn_generic/service/gmn.wsgi

    DocumentRoot /var/local/mn/mn_generic/service

    <Directory /var/local/mn/mn_generic/service>
      WSGIApplicationGroup %{GLOBAL}
      Order deny,allow
      Allow from all
    </Directory>

  </VirtualHost>
