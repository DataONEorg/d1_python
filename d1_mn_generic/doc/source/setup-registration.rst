Register the new Member Node with DataONE
=========================================

Before a Member Node can participate in the DataONE infrastructure, it must be
registered. Registering the MN involves the following steps:

#. Creating a DataONE identity in the environment that was selected in the
   :doc:`setup-env` step.

#. Obtaining a client side certificate from DataONE. The certificate enables the
   MN to authenticate itself in the environment.

#. Submitting a Node document. The Node document describes the MN and
   the level at which it will participate in the DataONE infrastructure

#. DataONE evaluates the submission. Upon approval, the registration is
   complete, and the Node is part of the DataONE infrastructure.

Perform the steps in order, as each step depends on earlier steps.


Create a DataONE identity
~~~~~~~~~~~~~~~~~~~~~~~~~

Use the DataONE Identity Manager to create a DataONE identity for the
administrator / contact for the new MN.

  Visit **<environment-url>**/portal/ and follow the instructions.


Registering the MN with DataONE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GMN generates the Node document automatically based on the settings in
``settings_site.py``.

    Create a copy of the GMN settings template and edit the settings::

      $ cd /var/local/dataone/gmn/lib/python2.6/site-packages/service
      $ sudo cp settings_site_template.py settings_site.py

Django requires a unique, secret key to be set up for each application.

  Generate a random string::

    $ openssl rand -base64 32

  * Copy the string to the clipboard.

  * Edit ``settings_site.py``.

  Modify the following settings:

  * SECRET_KEY: Replace 'MySecretKey' with the string that was generated in
    the previous step.

  * NODE_IDENTIFIER: Select a short string that will uniquely designate your
    node in the DataONE infrastructure.

  * NODE_NAME: Select a name for your node.

  * NODE_DESCRIPTION: Select a brief description for your node.

  * NODE_BASEURL: Specify the URL at which your node will be available.

  * NODE_SUBJECT: Specify the subject for this node (retrieved from the client
    certificate provided by DataONE)

  * NODE_CONTACT_SUBJECT: Specify the subject that was submitted as the
    contact person for DataONE.

  * DATAONE_ROOT: Select the environment that matches the one that was
    selected in :doc:`setup-env`.

  * PASSWORD: Set the password that was selected for the gmn user in
    :doc:`setup-postgresql`.

  * Edit
    ``/var/local/dataone/gmn/lib/python2.6/site-packages/service/settings_site.py``
    setting.

  After editing ``settings_site.py``, check if the Node document is successfully
  generated::

    $ su gmn
    $ cd /var/local/dataone/gmn
    $ . bin/activate
    $ python lib/python2.6/site-packages/service/manage.py register_node_with_dataone --view

  If the Node document is successfully generated, an XML document will be
  displayed. For more information about this document, refer to
  http://mule1.dataone.org/ArchitectureDocs-current/apis/Types.html#Types.Node

  When the Node document is successfully generated and displayed, register the
  MN by submitting the Node document to DataONE. The Node document is
  automatically submitted to DataONE over a TLS/SSL connection that has been
  authenticated with the certificate obtained above::

    $ python lib/python2.6/site-packages/service/manage.py register_node_with_dataone

A new MN must be approved by DataONE. The person that is registered as
*contactSubject* in the Node document, will be contacted by email with the
outcome of the approval process. After the Node has been approved, the Node is
part of the DataONE infrastructure and CNs will start processing the information
on the node.
