SSL/TLS Troubleshooting
=======================

Commonly seen OpenSSL SSL/TLS connection errors and X.509 client or server side certificate configuration errors with possible causes and solutions.

#### Error Code 1

`SSLError(SSLError(1, '[SSL: TLSV1_ALERT_UNKNOWN_CA] tlsv1 alert unknown ca (_ssl.c:2273)'),`
`ssl.SSLError: [Errno 1] _ssl.c:510: error:14094418:SSL routines:SSL3_READ_BYTES:tlsv1 alert unknown ca`
`SSLError(SSLError("bad handshake: Error([('SSL routines', 'ssl3_read_bytes', 'tlsv1 alert unknown ca')],)",),)`

Cause:

* Client connected using a cert that was signed by a CA unknown to the server
* Apache was unable to find the root CA cert that was used for signing the client side cert in its local store of trusted root CA certs
* Apache was also unable to find intermediate certs that could be used for creating a chain from the client side cert to one of the root CA certs

Check:

* Check that the CA used for signing the client side cert is set up to be trusted by Apache

* The signing CA should either be in a folder pointed to by `SSLCACertificatePath` or in a cert bundle file pointed to by `SSLCACertificateFile`
  * Typical location of these settings is `gmn2-ssl.conf`

* For client side certs signed by DataONE, point `SSLCACertificateFile` to local copy of cert bundle:
  * Test environments: https://repository.dataone.org/software/tools/trunk/ca/DataONETestCAChain.crt
  * Production: https://repository.dataone.org/software/tools/trunk/ca/DataONECAChain.crt

* For self signed client side certs, copy the signing CA cert to the directory pointed to by `SSLCACertificatePath` then run the `c_rehash` command in that directory.

* If the signing CA cert is in the right location, but seems to be ignored, check that the symbolic links containing hash values for the CA certs are present. If necessary, create them with the `c_rehash` command

* If any intermediate certs are required in order to connect the client side cert with a root CA cert, check that they are present. They should be installed just like root CA certs

* If client is connecting to a DataONE environment, check that the connection is to the env for which the client side cert was issued
  * DataONE uses `urn_node_<NAME>` for production certs and `urn_node_mnTest<NAME>` for test certs. E.g., in `settings.py`:
    * `DATAONE_ROOT = d1_common.const.URL_DATAONE_ROOT` -> `CLIENT_CERT_PATH = 'urn_node_<NAME>'`
    * `DATAONE_ROOT = 'https://cn-stage.test.dataone.org/cn'` -> `CLIENT_CERT_PATH = 'urn_node_mnTest<NAME>'`

* Check that the root CA certs are valid and PEM encoded
  * View the cert files with `openssl x509 -in <cert_file.pem> -text -noout`

#### Certificate verify failed

`SSLError: ("bad handshake: Error([('SSL routines', 'ssl3_get_server_certificate', 'certificate verify failed')],)",`
`(SSLError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)'),))`

Cause:

* Client received a certificate that the client was unable to validate

Check:

* Check that the server side cert was signed by a CA known to the client and has not expired
* Check that the system clock on the client system is correct

#### Operation timed out

`ssl.SSLError: ('The write operation timed out',)`
`ssl.SSLError: ('The read operation timed out',)`
`SSLError: _ssl.c:495: The handshake operation timed out`

Cause:

* Client timed out while waiting for response from server

Check:

* Increase the timeout on the client
* Consider using streaming HTTP requests and responses

