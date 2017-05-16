Setup GMN Vhost & SSL Configuration
===================================

First we will remove default SSL.conf and add a custom config virtual host file. The basic unit of configuration for an individual website is called a
“virtual host” or “vhost”. A virtual host directive will let the server know where to find your site’s files, where you want log files to go, which port the configuration applies to, and can contain a variety of other instructions for how the web server should handle this site. For your convenience, a virtual host file is already provided with your GMN installation files.

Remove the default ssl.conf file containing a default vhost::

    $ cd /etc/httpd/conf.d/
    $ sudo rm ssl.conf


Copy over and edit gmn2-ssl.conf virtual host file::

    $ sudo cp /var/local/dataone/gmn_venv/lib/python2.7/site-packages/gmn/deployment/gmn2-ssl.conf /etc/httpd/conf.d/
    $ sudo vi gmn2-ssl.conf

Change the ServerName to your domain, which should already be pointed at your server’s IP. This must be consistent with the domain as it will be expressed when registering an SSL certificate.


Change server admin to appropriate email contact.


Replace {$APACHE_DIR} in log file declarations with “logs” because that is defined for Apache on Debian. So the log declarations should read::

        ErrorLog                logs/error.log
        CustomLog               logs/access.log combined

Add the below text to the top of the file, above the start of the
<IfModule mod_ssl.c> directive and Virtualhost entry. This is basically combining the default ssl.conf configurations with the GMN virtual host configuration::

    LoadModule ssl_module modules/mod_ssl.so

    # These lines come from the default ssl.conf file:
    Listen 443 https
    SSLPassPhraseDialog exec:/usr/libexec/httpd-ssl-pass-dialog
    SSLSessionCache         shmcb:/run/httpd/sslcache(512000)
    SSLSessionCacheTimeout  300
    SSLRandomSeed startup file:/dev/urandom  256
    SSLRandomSeed connect builtin
    SSLCryptoDevice builtin

    # Disable for protection against vulnerabilities such as POODLE.
    SSLProtocol all -SSLv3 -SSLv2

    SSLCipherSuite "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA RC4 !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS !RC4"

Load additional config file for http to https forwarding in the "/etc/httpd/conf.d" directory::

    $ sudo cp /var/local/dataone/gmn_venv/lib/python2.7/site-packages/gmn/deployment/forward_http_to_https.conf /etc/httpd/conf.d/

Don’t try to restart apache yet!
Ordinarily, one might expect to restart apache at this point. However, the custom .conf file just copied over contains several references to certificate files and directories we have not yet created, so a restart would fail at this point.
