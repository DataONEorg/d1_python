Overview of operation
=====================

The DataONE Command Line Interface enables basic interactions with the DataONE infrastructure via the command line.


.. _session:

Session
~~~~~~~

The CLI is built around the concept of session variables. Session variables are analogous to environment variables in an operating system. The session variables store information that is often reused by multiple commands and minimize the amount of typing that is required. For instance, one session variable is the Base URL to a Member Node. Whenever a command is typed that will access a Member Node, the URL for the Member Node is pulled from the session.

The session can be saved and loaded from files. This allows easy switching between different roles by the user. For instance, if a user often works with two different Member Nodes and creates different types of objects on them, he can save the session after setting it up for each role, after which he can easily switch between them by loading the appropriate session.


.. _read_write_operations:

Read vs. write operations
~~~~~~~~~~~~~~~~~~~~~~~~~

The commands that cause operations to be issued against Coordinating Nodes and Member Nodes are divided into two broad categories; read commands and write commands. These two categories are handled differently by the CLI. Read operations are issued immediately and their results displayed on screen or saved to a file. Write operations, however, are added to a queue, called the write operation queue, to be issued later.


.. _write_operation_queue:

Write operation queue
~~~~~~~~~~~~~~~~~~~~~

The DataONE infrastructure does not allow science objects to be modified or deleted once created. Objects can be updated, but the original object stays in the system forever. The write operation queue allows operations to be viewed and edited, thus adding a buffer where mistakes, such as typos, can be caught before the permanent operations are issued.

Like read commands, write commands use session variables. Each time an operation is added to the write operation queue, the relevant session variables are used for creating parameters for the operation. When an operation is later issued, it uses the parameters stored in the operation, not the current session variables.

When the commands have been verified, the queue is issued with a single command, after which each of the operations in the queue are automatically performed in sequence. If any operation fails, the process is stopped. The failed operation and all subsequent operations remain in the queue and can be manipulated before the queue is issued again. The successfully performed operations cannot be undone.


.. _access_policy:

Access Policy
~~~~~~~~~~~~~

The Access Policy is a list of subjects and their associated access levels. The Access Policy is applied to new objects as they are created. The Access Policy can also be updated on existing Science Data Objects.


.. _replication_policy:

Replication Policy
~~~~~~~~~~~~~~~~~~

The Replication Policy contains a list of Member Nodes that are specifically preferred or blocked as replication targets. The Replication Policy also contains a setting that specifies if replication is allowed or disallowed, and the preferred number of replicas.

The Replication Policy is applied to new objects as they are created. The Replication Policy can also be updated on existing Science Data Objects.

The DataONE infrastructure will never replicate an object to a Member Node that is in the list of blocked Member Nodes for that object. If a Member Node is added to the list of blocked Member Nodes after an object has been replicated to that Member Node, the DataONE infrastructure will request that the Member Node in question remove its copy of the object.

If the preferred number of replicas is larger than the number of Member Nodes that have been specified as preferred replication targets, additional Member Nodes that are not in the blocked list will automatically be selected as replication targets.

If the preferred number of replicas is modified on an existing Science Data Object, DataONE will adjust the number of existing replicas by creating and deleting replicas of that object as needed.


.. _authentication:

Authentication
~~~~~~~~~~~~~~

A user that accesses a :term:`Node` may connect either anonymously or as an authenticated subject. The Node to which the user connects will allow access to operations, Science Objects and other data based on the permissions that have been granted to the subject for which the user has authenticated.

A user that connects anonymously is granted access only to publicly available operations and data. Access is typically denied for operations that create or update data, such as the :ref:`create <create>` operation.

When the CLI connects to a Node on a user's behalf, it passes authentication information for that user via a :term:`certificate`. The certificate enables the user to act as a specific subject within a Node.

The user obtains a certificate for the subject with which to access a Node from
:term:`CILogon`. When the user downloads a certificate from CILogon, the CILogon download process stores the certificate in a standard location. The CLI can automatically find certificates in this location. In some cases, certificates may be stored in custom locations. In such cases, the automatic location of certificates can be bypassed by setting the :ref:`cert-path <cert-path>` session parameter to the filesystem path of the certificate. Because CILogon provides a certificate that holds both the public and private keys in the same file, only
:ref:`cert-path <cert-path>` is required and :ref:`key-path <key-path>` should be set to None. If the certificate was obtained in some other way, and the certificate's private key is stored in a separate file, the :ref:`key-path
<key-path>` session parameter must be set to the filesystem path of the private key.

When a user types a command that requires the CLI to connect to a Node, the CLI starts by examining the value of the the :ref:`anonymous <anonymous>` session parameter. If the :ref:`anonymous <anonymous>` session parameter is **True**, the CLI ignores any available certificate and connects to the DataONE Node without providing a certificate. This causes the Node to allow access only to publicly available operations and data.

If the :ref:`anonymous <anonymous>` session parameter is **False**, the CLI attempts to locate the user's certificate as described above. If a certificate is not found, the operation is aborted. If a certificate is found, the CLI passes the certificate to the Node when establishing the connection. The Node validates the certificate and may reject it, causing the operation to be aborted. If the certificate is successfully validated, the Node grants access to the user, authenticated as the subject designated in the certificate, and the CLI proceeds with the operation.
