.. _authentication:

Authentication
--------------

A user that accesses a :term:`Node` may connect either anonymously or as an
authenticated subject. The Node to which the user connects will allow access to
operations, Science Objects and other data based on the permissions that have
been granted to the subject for which the user has authenticated.

A user that connects anonymously is granted access only to publicly available
operations and data. Access is typically denied for operations that create or
modify data, such as the :ref:`create <create>` operation.

When the CLI connects to a Node on a user's behalf, it passes authentication
information for that user via a :term:`certificate`. The certificate enables the
user to act as a specific subject within a Node.

The user obtains a certificate for the subject with which to access a Node from
:term:`CILogon`. When the user downloads a certificate from CILogon, the CILogon
download process stores the certificate in a standard location. The CLI can
automatically find certificates in this location. In some cases, certificates
may be stored in custom locations. In such cases, the automatic location of
certificates can be bypassed by setting the :ref:`certpath <certpath>` session
parameter to the filesystem path of the certificate. Because CILogon provides a
certificate that holds both the public and private keys in the same file, only
:ref:`certpath <certpath>` is required and :ref:`keypath <keypath>` should be
set to None. If the certificate was obtained in some other way, and the
certificate's private key is stored in a separate file, the :ref:`keypath
<keypath>` session parameter must be set to the filesystem path of the private
key.

When a user types a command that requires the CLI to connect to a Node, the CLI
starts by examining the value of the the :ref:`anonymous <anonymous>` session
parameter. If the :ref:`anonymous <anonymous>` session parameter is **True**,
the CLI ignores any available certificate and connects to the DataONE Node
without providing a certificate. This causes the Node to allow access only to
publicly available operations and data.

If the :ref:`anonymous <anonymous>` session parameter is **False**, the CLI
attempts to locate the user's certificate as described above. If a certificate
is not found, the operation is aborted. If a certificate is found, the CLI
passes the certificate to the Node when establishing the connection. The Node
validates the certificate and may reject it, causing the operation to be
aborted. If the certificate is successfully validated, the Node grants access to
the user, authenticated as the subject designated in the certificate, and the
CLI proceeds with the operation.

