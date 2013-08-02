Examples
========

.. note:: Use the Arrow Up and Arrow Down keys to find commands in the command
  history. These can then be edited and run again.


Viewing and manipulating the session variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Viewing and manipulating the :ref:`session variables <session_variables>`
used when performing operations against the :term:`DataONE` infrastructure
via the DataONE Command Line Interface (CLI).

If desired, the session variables can be :ref:`reset` back to their defaults
(useful if they were modified by an existing ``.dataone_cli.conf`` file at
startup)::

  > reset

Set the authentication session variables for authenticated access using a
certificate from CILogon (downloaded to the default location in /tmp)::

  > set anonymous false
  > set cert-file none
  > set key-file none

Or set to use a certificate in a non-standard location:

  > set cert-file /etc/dataone/client/certs/myclientcert.pem

View all the session variables::

  > set

Save the session variables to a file for later use::

  > save ~/d1/mysettings

Exit the CLI::

  > exit


Searching for Science Data
~~~~~~~~~~~~~~~~~~~~~~~~~~

A scientist can discover and download Science Data to leverage them in
their own research.

Load the session variables from the file created in the previous step::

  > load ~/d1/mysettings

View the session variables::

  > set

Perform an unlimited search::

  > set query *:*
  > search

Restrict the search to a specific time or later::

  > set from-date 1998-01-01T05:00:00
  > search

Modify the search parameters to find only Science Data that originated from
the "DEMO3" :term:`MN` and search::

  > set query origin_mn:DEMO3
  > search

The search terms can also be specified after the "search" command::

  > search barnacle

Modify the search parameters to find only Science Data that are of type
text/csv and search again::

  > set format-id text/csv
  > search barnacle


Downloading Science Data Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

View the session variables::

  > set

Set :term:`MN` from which to download the Science Data Object::

  > set mn-url https://dataone.member.node.com/mn/

Download Science Data Object and save to local file::

  > get hdl:10255/dryad.669/mets.xml ~/my_dataone_files/dryad669.xml



Downloading System Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~

System Metadata is an XML document that contains additional information about
a Science Data Object.

Retrieve the System Metadata and display it::

  > meta hdl:10255/dryad.669/mets.xml

Retrieve the System Metadata and save it to a file::

  > meta hdl:10255/dryad.669/mets.xml ~/d1/dryad669_system_metadata.xml



Downloading an access restricted object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Authenticate with CILogon, at https://cilogon.org/?skin=DataONE

Tell the CLI that you wish to use authentication::

  > set anonymous False

* Download an object for which you have read access::

  > get my-access-controlled-identifier

See :doc:`ref_auth` for more information.



Uploading Science Data Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A scientist can upload a set of Science Data to benefit from the services
provided by DataONE.

Select :term:`MN` to which to upload the Science Data Object::

  > set mn-url https://dataone.member.node.com/mn/

Configure the session variables used when generating :term:`System Metadata`::

  > set rights-holder CN=MATTJTEMP,DC=dataone,DC=org
  > set origin-mn DEMO1
  > set authoritative-mn DEMO1

Create an Access Policy that has only public read permisisons::

  > clearaccess
  > allowaccess public read

Add a create (upload) operation of the Science Data Object to the write operation queue::

  > create mynewpid ~/path/to/my/file

View the queue::

  > queue

Edit the queue if there are any mistakes in the create operation::

  > edit

Perform all operations in the queue::

  > run

Store the settings in ``.dataone_cli.conf`` for use when creating similar
Science Data Objects later::

  > save

Exit the CLI::

  > exit


Misc operations
~~~~~~~~~~~~~~~

Find replicas of Science Data Objects::

  > resolve hdl:10255/dryad.669/mets.xml

Display list of Science Data Objects on a :term:`MN` or :term:`CN`::

  > set mn-url https://mn.dataone.org/mn
  > set start 100
  > set count 10
  > list

Display event log on a :term:`MN`::

  > reset
  > set anonymous false
  > set cert-file /etc/dataone/client/certs/myclientcert.pem
  > set key-file None
  > set mn-url https://dataone.org/mn
  > log

Download the event log and save it to a file::

  > log events.xml
