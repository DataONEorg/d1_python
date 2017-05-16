Install Server SLL Certificate
===================================

SSL certificates accomplish several things. For example, they provide for encrypted communication. They also support a feature whereby browsers will recognize whether or not a server’s SSL certificate has come from a trusted Certificate Authority.

These instructions cover three options for handling server SSL certificates. Please review all three options and select the one that is most appropriate for your installation.

Option 1: Install an Externally Generated SSL Cert from a Trusted CA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Either you or your IT department may have already acquired an SSL certificate registered for the domain that is pointing to the server where you are installing GMN. If so, then just create the directory::

    $ sudo mkdir -p /var/local/dataone/certs/server

 And copy your server certificate and corresponding key into it.


Option 2: Create a Self-Signed SSL Cert for Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is possible to create a self-signed certificate. While this certificate will not be trusted by browsers, it will still be useful for testing that our SSL configurations are working. The below command will generate the certificate and key, putting them in the location where the gmn2-ssl.conf file has been told to look for it::

    $ sudo mkdir -p /var/local/dataone/certs/server
    $ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /var/local/dataone/certs/server/server_key_nopassword.pem -out /var/local/dataone/certs/server/server_cert.pem

You will be asked to enter some information as shown below. Be sure to enter the domain being pointed at your server's IP for the Common Name. Don't forget that this should be consistent with the domain we configured as the ServerName in the gmn2-ssl.conf file::

    Country Name (2 letter code) [XX]:US
    State or Province Name (full name) []:Tennessee
    Locality Name (eg, city) [Default City]:Oak Ridge
    Organization Name (eg, company) [Default Company Ltd]:GMN Test Org
    Organizational Unit Name (eg, section) []:
    Common Name (eg, your name or your server's hostname) []:gmn.example.edu
    Email Address []: admin@example.edu


At this point you should be able to navigate to your domain in a browser or with curl and see the apache default webpage. If using a browser, you'll have to exception the security complaint, as the browser won't trust a self-signed certificate as secure. If using curl, you'll need to add the --insecure option. For example::

    $ curl --insecure https://gmn.example.edu



Option 3: Create and Install a Free Cert using Let's Encrypt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don’t have a certificate from a CA yet, you can make one for free. Let’s Encrypt is “a free, automated, and open certificate authority (CA), run for the public’s benefit”. It is widely gaining traction as an alternative to the traditionally pricey cost of SSL certificates from trusted Certificate Authorities. More information is available at https://letsencrypt.org/. This section will walk you through the steps of acquiring an SSL Cert from Let’s Encrypt. The instructions assume that (A) you have already pointed your domain/subdomain at the installation server, and (B) the virtual host for the domain has already been configured in the web server.

A package called Certbot is the easiest way to generate a certificate using Let's Encrypt. Certbot is found in EPEL (Extra Packages for Enterprise Linux). To use Certbot, you must first enable the EPEL repository::

    $ sudo yum install epel-release

Install Certbot::

    $ sudo yum install python-certbot-apache

Certbot has a fairly solid beta-quality Apache plugin, which is supported on many platforms, and automates both obtaining and installing certs. To generate the certificate::

    $ sudo certbot --apache -d gmn.example.edu

You will be asked to enter a contact email. Choose the https only option when you get to that part. After the script is finished, you should be provided a link you can use to test your SSL configurations, such as::

    -------------------------------------------------------------------------------
    Congratulations! You have successfully enabled https://centos7-3gmn.kitty.ninja

    You should test your configuration at:
    https://www.ssllabs.com/ssltest/analyze.html?d=gmn.example.edu
    -------------------------------------------------------------------------------

Clicking on that link will take you to a recommended tool by SSL labs which will provide a rating for your server’s SSL configurations. Following the recommended configurations outlined in these instructions should result in getting an A rating. If you get less than that, feel free to ask for suggestions on how to improve your rating.

Use the following command to show information about the certificate that was generated::

    $ sudo certbot certificates

Which will provide output similar to::

    -------------------------------------------------------------------------------
    Found the following certs:
      Certificate Name: gmn.example.edu
        Domains: gmn.example.edu
        Expiry Date: 2017-06-21 18:22:00+00:00 (VALID: 89 days)
        Certificate Path: /etc/letsencrypt/live/gmn.example.edu/fullchain.pem
        Private Key Path: /etc/letsencrypt/live/gmn.example.edu/privkey.pem
    -------------------------------------------------------------------------------





However, you should not need to update your vhost with this information. If you go back and look at the contents of the GMN virtual host file::

	$ vi /etc/httpd/conf.d/gmn2-ssl.conf

You’ll see that the paths for SSLCertificateFile and SSLCertificateKeyFile have automatically been updated for you.