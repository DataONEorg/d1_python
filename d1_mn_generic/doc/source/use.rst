Using GMN
=========

After :term:`GMN` has been set up according the setup instructions, it exposes
the complete REST interface that DataONE has defined for Member Nodes.
Currently, the easiest way to interact with GMN is to use the DataONE Command
Line Client (CLI). The CLI is installed automatically with GMN and can be
started by typing "dataone". The CLI can also be scripted to perform tasks such
as bulk object creations to populate an instance of GMN with science data.

If more comprehensive access to the node is required, DataONE provides libraries
in Java and Python that simplify the process of interacting with DataONE Member
Nodes and Coordinating Nodes. The libraries can be used as foundations for
custom applications that use the DataONE infrastructure.


Populating your new node
~~~~~~~~~~~~~~~~~~~~~~~~

The DataONE Client Library for Python includes an example on how to iterate over
a set of files, create data packages (resource maps) for them, and upload them
to a Member Node.


Authenticating to your node
---------------------------

To authenticate to your node, you must connect over HTTPS and provide a
certificate. The certificate must be issued by CILogon or DataONE (the two CAs
that a Member Node trusts by default). In addition, the certificate must be for
a subject that has the rights required for performing the operation(s) the
client intends to perform after connecting. For instance, GMN requires that the
subject used in connections that create content on the node validate against an
internal whitelist.

When running operations against the node as a regular user, it is natural to
a certificate obtained from from CILogon. CILogon provides certificates that
are secured by a having a time limit of 18 hours.

However, when running an automated task, such as a task that connects to the
Node once a day and creates new objects, the CILogon certificate is not a good
fit, as someone would have to manually update the certificate every day. There
are two basic ways to resolve this:

1) Use the certificate that was issued to the node by DataONE. GMN automatically
trusts this certificate. However, there are security implications to this.
Anyone that gains access to this certificate can access all the content on your
node and can act as your node in the DataONE infrastructure. So, it's best to
only use this approach when running the automated tasks on the same server on
which GMN runs, or from another tightly controlled server. To use the DataONE
issued certificate in local connections, simply provide the paths to the
certificate and its private key in ``/var/local/dataone/certs/client`` when
creating a Member Node client in script.

2) Set up a local CA. This is the only option if the node has been set up as a
:doc:`stand-alone test instance <setup-local>`. This CA is then added to the CAs
trusted by GMN and used for issuing one or more certificates, which are then
used by the automated processes. This is the most secure solution as
certificates issued by your local CA cannot be used for representing you in the
DataONE infrastructure, should your local CA be compromised. See
:doc:`setup-local-ca` for instructions on how to set this up.


Vendor specific extensions
~~~~~~~~~~~~~~~~~~~~~~~~~~

GMN implements a set of extensions that enhance the functionality of GMN. Most
of these are designed to help with debugging and profiling and they are
described in another section.


Remote URL
----------

The Remote URL vendor specific extension enables GMN to be used for exposing
science data that is already available through another web based service without
having to create another copy of that data.

In the regular create() and update() REST calls, the bytes of the science
objects are provided, and the MN manages the storage of the science objects.
When using the Remote URL extension, the bytes of the objects are not provided
and instead, a HTTP or HTTPS URL to the original location of the data is
provided. GMN then manages all aspects of exposing the science data except for
the actual storage of the bytes of the exposed object.

When the object is downloaded from GMN, GMN streams the object from its original
location in the background.

This extension is activated by added an HTTP header to the REST call for
create() and update(). The name of the header is VENDOR_GMN_REMOTE_URL and the
value is the HTTP or HTTPS URL that references the object in the remote
location.
