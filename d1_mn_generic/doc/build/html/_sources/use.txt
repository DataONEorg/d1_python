Using GMN
=========

After :term:`GMN` has been set up according the setup instructions, it exposes
the complete REST interface that DataONE has defined for Member Nodes.
Currently, the easiest way to interact with GMN is to use the DataONE Command
Line Client (CLI). The CLI can also be scripted to perform tasks such as bulk
object creations to populate an instance of GMN with science data for exsposure
to DataONE.

If more comprehensive access to the node is desired, DataONE provides libraries
in Java and Python that simplify the process of interacting with DataONE. The
libraries can be used as foundations for custom applications that use the
DataONE infrastructure.


Vendor specific extensions
~~~~~~~~~~~~~~~~~~~~~~~~~~

GMN implements a set of extensions that expand the functionality of GMN. Most of
these are designed to help with debugging and profiling and they are described
in another section.


Remote URL
----------

The Remote URL vendor specific extension enables GMN to be used for exposing
science data that is already available through another web based service without
having to create another copy of that data.

In the regular create() and update() REST calls, the bytes of the science
objects are provided, and the MN manages the storage of the science objects.
When using the Remote URL extension, the bytes of the objects are not provided
and instead, a HTTP or HTTPS URL to the original location of the data is
provided. GMN then managaes all aspects of exposing the science data except for
the actual storage of the bytes of the exposed object.

When the object is downloaded from GMN, GMN streams the object from its original
location in the background.

This extension is activated by added an HTTP header to the REST call for
create() and update(). The name of the header is VENDOR_GMN_REMOTE_URL and the
value is the HTTP or HTTPS URL that references the object in the remote
location.
