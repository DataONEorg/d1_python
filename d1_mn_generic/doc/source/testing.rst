Setting up testing and debugging environment for GMN
====================================================

In production, GMN is always served over SSL with an optional :term:`client side
certificate`. For testing and debugging, GMN must be served over HTTP because
the Django development server does not support HTTPS. In that scenario, it is
not possible for the client to provide a certificate.

.. graphviz::

   digraph G {
    production -> HTTPS -> Apache -> certificate -> GMN [color=green];
    production -> HTTPS -> Apache -> "no certificate" -> GMN [color=blue];

    debugging -> HTTP -> "Django dev server" -> "simulated certificate" -> GMN [color=red];
    debugging -> HTTP -> "Django dev server" -> "no certificate" -> GMN [color=orange];

    "integration tests" -> production;
    "integration tests" -> debugging;

    "browser" -> production;
    "browser" -> debugging;
  }

Figure: The various scenarios that GMN can be served under.

* Green: Production with client side certificate. Apache will reject the
  connection if the certificate is not valid, and GMN will not see the
  connection attempt. The certificate must be signed by :term:`CILogon`.

* Blue: Production without a client side certificate. Apache accepts the
  connection. GMN falls back to the default Public session.

* Red: Testing and debugging with simulated certificate. This path is used by
  the integration tests. Debugging is supported. Because HTTP is used, no
  certificate can be provided. Instead, a valid certificate is simulated by
  using a Vendor Specific Extension to pass in a session. 
  
  Because Apache rejects connections with invalid certificates in production,
  there is no need to simulate a scenario where an invalid certificate is
  passed to GMN.

  This path is only available when GMN is running in debug mode.

* Orange: Testing and debugging without a certificate. Same as the testing path
  with simulated certificate except that it simulates a connection without a
  session by not providing a session in the Vendor Specific Extension. This
  requires GMN to fall back to the default Public session.

* From the point of view of GMN, there are 3 types of connections:

  #. Connection with valid certificate
  #. Connection without certificate (accepted, fall back to Public)
  #. Connection with simulated certificate (accepted only in debug mode)
  

Integration tests against production instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<TODO: Add instructions on how to run the integration tests with a valid
certificate signed by CILogon>


Integration tests against debug instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The integration tests are by deafult set up to assume that the GMN instance they
connect to is in debug mode and they should all pass without any additional
configuration.


Browser testing against production instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases, it's convenient to test GMN via a browser though only the GET
based REST calls are conveniently reproducible from a browser. These
instructions focus on `Firefox <http://www.mozilla.com/firefox>`_.

GMN will authenticate with a :term:`server side certificate` signed by CILogon.
Set the browser up to accept this certificate by adding the CILogon CA
certificates to the browser's trusted CA store:

* Open the Certificate Manager (Edit | Preferences | Advanced | Encryption |
  View Certificates)
* Import new CA (Authorities | Import)
* Browse to /var/local/dataone/ca/cilogon-basic.pem
* Select "Trust this CA to identify web sites."

Repeat with the ``cilogon-openid.pem`` and ``cilogon-silver.pem`` certificates.

The functionality accessible by the Public principal through GET based REST
calls can now be tested.

To test functionality accessible only to authenticated users, the browser must
be set up to provide a valid certificate signed by CILogon.

<TODO: Add instructions on how to obtain a certificate from CILogon and install
it in Firefox>


Browser testing against debug instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In debug mode, GMN supports providing a simulated certificate via :term:`vendor
specific extensions`. In this mode, the session object that a certificate would
normally contain is passed to GMN via a custom HTTP header. To enable Firefox to
provide the header, install a Firefox extension such as `Modify Headers
<https://addons.mozilla.org/en-us/firefox/addon/modify-headers/>`_.

<TODO: Add instructions on how to use the Modify Headers extension to add a
simulated certificate>


Uploading test objects
~~~~~~~~~~~~~~~~~~~~~~

The create() call accept a :term:`vendor specific extensions` called
VENDOR_TEST_OBJECT. When this parameter is provided, the system metadata for
the object is accepted without any information being added or overwritten by
the MN.

