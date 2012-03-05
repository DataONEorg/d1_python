Register the MN
===============

Each DataONE Node has an XML document associated with it that describes the
various aspects of the Node, such as its URL, the services it supports and who
maintains and runs the Node. For now, it is necessary to manually edit this
file. A template is provided to simplify this process.

  Customize the Node XML document.

  Copy the Node XML template::

    $ cd /var/local/dataone/mn_generic/service/stores/static/
    $ cp nodeRegistry_template.xml nodeRegistry.xml

  Edit the XML document:

    Refer to
    http://mule1.dataone.org/ArchitectureDocs-current/apis/Types.html#Types.Node
    for descriptions of the fields in the XML document. Then replace the upper
    case texts with information specific to your MN. The parts of the document
    that do not contain upper case text should remain unchanged.

    Edit ``/var/local/dataone/mn_generic/service/stores/static/nodeRegistry.xml``.

To register the new MN with DataONE, the Node XML document is submitted,
together with an associated client side certificate, to a specific CN REST API.
A command line tool is provided for submitting the registration.

  Use the DataONE identity manager to create a DataONE identity for the
  administrator of the new MN::

    In a test install of GMN, this step is not neccessary.

    <TODO: Document this step>

  Visit CILogon to obtain a client side certificate for your DataONE identity:

  Open a browser and go to URL: https://cilogon.org/?skin=DataONE

  Follow the prompts. Note the file path of your new certificate.

  Register the MN with DataONE::

    $ cd /var/local/dataone/mn_generic/tools
    $ python register.py --cert-path <path to your certificate> ../service/stores/static/nodeRegistry.xml

A new MN must be approved by DataONE. The person that submitted the registration
will be contacted by email with the outcome of the approval process.


Revisit the GMN configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the :doc:`setup-d1-gmn` step, setting the NODE_IDENTIFIER value was deferred
because it must be set up to match the value configured in this step.

  Edit: ``/var/local/dataone/mn_generic/service/settings_site.py``

  * Set NODE_IDENTIFIER to match the value specified in the identifier field
    in the Node XML document.


:doc:`setup-workers`
