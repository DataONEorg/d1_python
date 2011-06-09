Setting testing environment up for GMN
--------------------------------------

We need GMN to accept two certificates for testing.

Creat self signed certificate::
  Apache self signed certificate HOWTO
  http://www.perturb.org/display/entry/754/
  / ca.key pass phrase: test
  As DN, I put my IP number (this probably only needs to be done in the root cert)
  server.key pass phrase: test
  challenge password: <blank>
  Performed the optional step to remove the password.
  Skipped Apache config step.

Copy the server.crt and server.key.nopass files into standard location (for Ubuntu).

  mkdir /etc/apache2/ssl
  cp server.crt /etc/apache2/ssl
  cp server.key /etc/apache2/ssl


~~~~~~~

CILogon.

The downloaded .p12 file contains a certificate that includes the private key.

$ chmod 0600 usercred.p12
Convert from P12 to PEM

The "Get New Certificate" button at https://cilogon.org provides a link to your
certificate and private key in PKCS12 (P12) format. To convert it to PEM format
for OpenSSL-based applications, use the openssl command:

$ openssl pkcs12 -in usercred.p12 -nokeys -out usercert.pem
$ openssl pkcs12 -in usercred.p12 -nocerts -out userkey.pem


~~~~~~

