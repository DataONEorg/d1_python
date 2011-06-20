Glossary
========

.. glossary::

  DataONE
    Data Observation Network for Earth

    https://dataone.org


  DataONE Common Library for Python
    Part of the DataONE :term:`Investigator Toolkit (ITK)`. Provides
    functionality commonly needed by projects that interact with the
    :term:`DataONE` infrastructure via Python. It is a dependency of
    :term:`DataONE Client Library for Python`, :term:`GMN` and all other DataONE
    components written in Python.


  DataONE Client Library for Python
    Part of the DataONE :term:`Investigator Toolkit (ITK)`. Provides
    programmatic access to the DataONE infrastructure and may be used to form
    the basis of larger applications or to extend existing applications
    to utilize the services of DataONE.


  GMN
    DataONE Generic Member Node

    GMN is an implementation of a :term:`MN`. It provides an implementation
    of all MN APIs. GMN can be used as a as a workbone or as a reference for a
    3rd party MN implementation. GMN can also be used as an "adapter", making it
    possible for a 3rd party system to become a MN and expose its objects to
    DataONE with a minimum of effort. In this mode, we refer to GMN as the
    adapter and the 3rd party system as the adaptee.

    When used as an adapter, GMN provides a minimal REST API that the adaptee
    can call into to expose its objects, in a process we refer to as object
    registration. After registration, GMN exposes objects on behalf of the
    adaptee.


  Vendor specific extensions
    Functionality that is not part of the DataONE APIs but is supported by
    a DataONE component. DataONE has defined APIs for accessing such extensions.


  Investigator Toolkit (ITK)
    The Investigator Toolkit provides a suite of software tools that are useful
    for the various audiences that DataONE serves. The tools fall in a number of
    categories, which are further developed here, with examples of potential
    applications that would fit into each category.

    http://mule1.dataone.org/ArchitectureDocs-current/design/itk-overview.html
    

  MN
    DataONE Member Node.


  CN
    DataONE Coordinating Node.

  
  client
    An application that accesses the DataONE infrastructure on behalf of
    a user.


  SciData
    An object (file) that contains scienctific observational data.


  SciMeta
    An object (file) that contains information about a SciData object.


  SysMeta
    An object (file) that contains system level information about a SciData or a
    SciMeta object.


  Subversion
    Version control system
    
    http://subversion.apache.org/


  Bash
    GNU Bourne-Again Shell
    
    http://www.gnu.org/software/bash/


  Apache
    HTTP server

    http://httpd.apache.org/


  Python
    A dynamic programming language.
    
    www.python.org
  

  Django
    High-level Python Web framework that encourages rapid development and clean,
    pragmatic design.

    https://www.djangoproject.com/


  WSGI
    Web Server Gateway Interface

    http://www.wsgi.org/wsgi/


  mod_wsgi
    An :term:`Apache` module that implements :term:`WSGI`.


  mod_ssl
    An :term:`Apache` module that interfaces to :term:`OpenSSL`.


  PyXB
    Python XML Schema Bindings
    
    http://pyxb.sourceforge.net/


  lxml
    A library for processing XML and HTML with Python
  
    http://lxml.de/


  minixsv
    A Lightweight XML schema validator
    
    http://www.familieleuthe.de/MiniXsv.html


  python-dateutil
    Extends the standard datetime module
    
    http://labix.org/python-dateutil


  python-setuptools
    A package manager for Python
  
    http://pypi.python.org/pypi/setuptools
  

  ISO8601
    International standard covering the exchange of date and time-related data
    
    http://en.wikipedia.org/wiki/ISO_8601

    
  python-iso8601
    Python library implementing basic support for :term:`ISO8601`
    
    http://pypi.python.org/pypi/iso8601/


  X.509  
    An ITU-T standard for a public key infrastructure (PKI) for single sign-on
    (SSO) and Privilege Management Infrastructure (PMI). X.509 specifies, amongst
    other things, standard formats for public key certificates, certificate
    revocation lists, attribute certificates, and a certification path validation
    algorithm.
  
    http://en.wikipedia.org/wiki/X509


  CA
    Certificate Authority
    
    A certificate authority is an entity that issues digital :term:`certificate`
    s. The digital certificate certifies the ownership of a public key by the
    named subject of the certificate. This allows others (relying parties) to
    rely upon signatures or assertions made by the private key that corresponds
    to the public key that is certified. In this model of trust relationships, a
    CA is a trusted third party that is trusted by both the subject (owner) of
    the certificate and the party relying upon the certificate. CAs are
    characteristic of many public key infrastructure (PKI) schemes.
    
    http://en.wikipedia.org/wiki/Certificate_authority


  CA signing key
    The private key which the :term:`CA` uses for signing :term:`CSR`\ s.
  
  
  Server key
    The private key that Apache will use for proving that it is the owner
    of the :term:`certificate` that it provides to the client during the
    SSL handshake.
    
  
  CSR
    Certificate Signing Request
    
    A message sent from an applicant to a :term:`CA` in order to apply for a
    :term:`certificate`. 

    http://en.wikipedia.org/wiki/Certificate_signing_request
    

  Certificate  
    A public key certificate (also known as a digital certificate or identity
    certificate) is an electronic document which uses a digital signature to bind
    a public key with an identity -- information such as the name of a person or an
    organization, their address, and so forth. The certificate can be used to
    verify that a public key belongs to an individual.
  
    http://en.wikipedia.org/wiki/Public_key_certificate


  CA certificate
    A certificate that belongs to a :term:`CA` and serves as the root
    certificate in a term:`chain of trust`.
    
    
  Self signed certificate
    A :term:`certificate` that is signed by its own creator. A self signed
    certificate is not a part of a :term:`chain of trust` and so, it is not
    possible to validate the information stored in the certificate. Because of
    this, self signed certificates are useful mostly for testing in an
    implicitly trusted environment.
  
    http://en.wikipedia.org/wiki/Self-signed_certificate


  Chain of trust
    The Chain of Trust of a Certificate Chain is an ordered list of
    certificates, containing an end-user subscriber certificate and intermediate
    certificates (that represents the Intermediate CA), that enables the
    receiver to verify that the sender and all intermediates certificates are
    trustworthy.

    http://en.wikipedia.org/wiki/Chain_of_trust

    
  OpenSSL
    Toolkit implementing the :term:`SSL` v2/v3 and :term:`TLS` v1 protocols as
    well as a full-strength general purpose cryptography library.


  SSL
    Secure Sockets Layer

    A protocol for transmitting private information via the Internet. SSL uses a
    cryptographic system that uses two keys to encrypt data − a public key known
    to everyone and a private or secret key known only to the recipient of the
    message.


  SSL handshake
    The initial negotiation between two machines that communicate over SSL.

    http://developer.connectopensource.org/display/CONNECTWIKI/SSL+Handshake
  
    http://developer.connectopensource.org/download/attachments/34210577/Ssl_handshake_with_two_way_authentication_with_certificates.png
    
    
  TLS
    Transport Layer Security

    Successor of :term:`SSL`.


  Client Side Authentication
    :term:`SSL` Client Side Authentication is part of the :term:`SSL handshake`,
    where the client proves its identity to the web server by providing a
    :term:`certificate` to the server. The certificate provided by the client
    must be signed by a :term:`CA` that is trusted by the server. Client Side
    Authentication is not a required part of the handshake. The server can be
    set up to not allow Client Side Authentication, to require it or to let it
    be optional.


  Server Side Authentication
    :term:`SSL` Server Side Authentication is part of the :term:`SSL handshake`,
    where the server proves its identity to the client by providing a
    :term:`certificate` to the client. The certificate provided by the server
    must be signed by a :term:`CA` that is trusted by the client. Server Side
    Authentication is a required part of the handshake.
  
  
  Client side certificate
    :term:`Certificate` that is provided by the client during :term:`client side
    authentication`.
  
  CILogon
    The CILogon project facilitates secure access to CyberInfrastructure (CI).
    
    http://www.cilogon.org/
    

  LOA
    Levels of Assurance
    
    CILogon operates three Certification Authorities (CAs) with consistent
    operational and technical security controls. The CAs differ only in their
    procedures for subscriber authentication, identity validation, and naming.
    These differing procedures result in different Levels of Assurance (LOA)
    regarding the strength of the identity contained in the certificate. For
    this reason, relying parties may decide to accept certificates from only a
    subset of the CILogon CAs.
    
    http://ca.cilogon.org/loa
  

  REST
    Representational State Transfer
    
    A style of software architecture for distributed hypermedia systems such as
    the World Wide Web.

    http://en.wikipedia.org/wiki/Representational_State_Transfer
    
  