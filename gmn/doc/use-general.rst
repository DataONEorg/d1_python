General
=======


Populating your new Node
~~~~~~~~~~~~~~~~~~~~~~~~

The DataONE Client Library for Python includes an example on how to iterate over a set of files, create data packages (resource maps) for them, and upload them to a Member Node. DataONE provides similar libraries for Java.

The CLI can also be scripted to perform tasks such as bulk object creations to populate a MN with Science Data.


Vendor specific extensions
~~~~~~~~~~~~~~~~~~~~~~~~~~

GMN implements a set of extensions that enhance the functionality of GMN. Most of these are designed to help with debugging and profiling and they are described in another section.


Remote URL
----------

The Remote URL vendor specific extension enables GMN to be used for exposing science data that is already available through another web based service without having to create another copy of that data.

In the regular ``MNStorage.create()`` and ``MNStorage.update()`` REST calls, the bytes of the science objects are provided, and the MN manages the storage of the objects. When using the Remote URL extension, the bytes of the objects are not provided and instead, a HTTP or HTTPS URL to the original location of the data is provided. GMN then manages all aspects of exposing the science data except for the actual storage of the bytes of the exposed object.

When the object is downloaded from GMN, GMN streams the object from its original location in the background.

This extension is activated by adding an HTTP header to the REST call for
``MNStorage.create()`` and ``MNStorage.update()``. The name of the header is
``VENDOR_GMN_REMOTE_URL`` and the value is the HTTP or HTTPS URL that references the object in the remote location. When this header is added, the section of the POST body that contains the object bytes is ignored, but it must still be included to form a valid REST call. It is typically set to contain a zero byte object.
