Test the installation
=====================

The new stand-alone GMN instance is now ready to be tested.

After a successful installation, GMN exposes
the `complete REST interface that DataONE has defined for Member Nodes
<http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html>`_.

The default installation makes GMN accessible both on the server's loopback
(localhost) and external interface(s). So the tests outlined below can be
performed on the local server or from a different host by replacing
``localhost`` with the server's external name or address.


Basic testing via web browser or curl
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These initial tests can be performed via a web browser or the ``curl`` command
line utility. By default, stand-alone instances of GMN use a non-trusted
"snakeoil" self-signed certificate. The browser will warn about this and may
require you to create a security exception. ``curl`` will need to be started
with the ``--insecure`` switch. For example, ``curl --insecure <url>``.

After the stand-alone GMN instance passes the tests, it can be joined to
DataONE by performing the :doc:`setup-env` section of the
installation, in which the non-trusted certificate is replaced with a publicly
trusted certificate from a 3rd party CA.


Node document
-------------

Open::

  https://localhost/mn/v1

You should see an XML document such as this:

.. code-block:: xml

  <?xml version="1.0" ?>
  <ns1:node replicate="true" state="up" synchronize="true" type="mn"
    xmlns:ns1="http://ns.dataone.org/service/types/v1">
    <identifier>urn:node:MyMemberNode</identifier>
    <name>My Member Node</name>
    <description>Test Member Node</description>
    <baseURL>https://localhost/mn</baseURL>
    <services>
      <service available="true" name="MNCore" version="v1"/>
      <service available="true" name="MNRead" version="v1"/>
      <service available="true" name="MNAuthorization" version="v1"/>
      <service available="true" name="MNStorage" version="v1"/>
      <service available="true" name="MNReplication" version="v1"/>
    </services>
    <synchronization>
      <schedule hour="*" mday="*" min="0/3" mon="*" sec="0" wday="?" year="*"/>
    </synchronization>
    <nodeReplicationPolicy>
      <spaceAllocated>10995116277760</spaceAllocated>
    </nodeReplicationPolicy>
    <subject>CN=urn:node:MyMemberNode,DC=dataone,DC=org</subject>
    <contactSubject>CN=My Name,O=Google,C=US,DC=cilogon,DC=org</contactSubject>
  </ns1:node>

This is your Node document. It exposes information about your Node to the
DataONE infrastructure. It currently contains only default values. The
:doc:`setup-env` section of the installation includes information
on how to customize this document for your node.


Home page
---------

GMN also has a home page with some basic statistics, available at::

  https://localhost/mn/home

Note that the ``home`` endpoint is not part of DataONE's API definition for
Member Nodes, and so does not include the DataONE API version designator
(``/v1/``) in the URL.


Testing via the DataONE Command Line Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DataONE provides the DataONE Command Line Client (CLI), a utility for
interacting with MNs and CNs. The CLI is installed automatically with GMN
and can be started by typing ``dataone`` while the gmn virtualenv is active.


Basic CLI usage
---------------

  Become the ``gmn`` user and activate the virtualenv::

    $ sudo su gmn; cd /var/local/dataone/gmn; . bin/activate;

  Start the CLI::

    $ dataone

  Get a list of commands::

    > help

  Get help on a specific command::

    > help list

  View the session variables::

    > set

  Save the settings::

    > save


Test anonymous connection
-------------------------

  If necessary, start the CLI as described above.

  Set your local GMN instance as the current target MN::

    > set mn-url https://localhost/mn

  Use an anonymous connection::

    > set anonymous true

  Perform a MNRead.listObjects() call, which will return a short XML document
  representing an empty list of objects::

    > list

  Save the settings::

    > save


Create and retrieve a test object
---------------------------------

GMN automatically assigns create, update and delete permissions to its own
client side certificate, so using GMN's client side certificate is a convenient
way of creating an authenticated connection that can be used for creating
objects on the node.

  If necessary, exit the CLI::

    > exit

  As the ``gmn`` user, create a text file containing the word "test"::

    $ echo >/tmp/test test

  Start the CLI::

    $ dataone

  Switch to an authenticated connection::

    > set anonymous false

  Use GMN's client side certificate for authentication::

    > set cert-file /var/local/dataone/certs/client/client_cert.pem
    > set key-file /var/local/dataone/certs/client/client_key_nopassword.pem

  Set the session variables that are required for creating the System Metadata
  for the new object::

    > set format-id text/plain
    > set authoritative-mn urn:node:MyMemberNode
    > set rights-holder testSubject

  Queue the object create operation::

    > create test /tmp/test

  View then execute the queued operation::

    > queue
    > run

  Press Enter to continue.

  Verify that the operation was executed successfully.

  Perform a MNRead.listObjects() call::

    > list

  Observe that the object list now contains an entry for the newly created
  object.

  Download the object::

    > get test /tmp/test2

  Save the settings and exit the CLI::

    > save
    > exit

  Verify that the downloaded object equals the original::

    $ cat /tmp/test /tmp/test2

  Remove the test files::

    $ rm /tmp/test /tmp/test2

See the `DataONE Command Line Interface (CLI) documentation
<http://pythonhosted.org/dataone.cli>`_ for more information about how to use
the CLI.

After successful completion of the tests above, the new GMN instance is ready
for stand-alone use. Usage scenarios for a stand-alone instance of GMN include
development and testing of DataONE clients and other DataONE infrastructure
components, evaluating performance and usability for some specific purpose and
learning about the infrastructure. Significant effort has been made in keeping
the implementation easy to read and extend as well.

As a DataONE MN, GMN also brings a unique mix of features that may make it
usable for object storage independent of DataONE. These features include X.509
certificate based authentication and authorization, SSL/TLS encryption, fine
grained ACL based access control for individual objects, basic tracking of
provenance and associated metadata such as Content-Type and checksum and a REST
API with libraries available for Java and Python.

Continue with the next installation section if the node is to be registered with
DataONE.
