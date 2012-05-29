Examples
========

.. note:: Instead of retyping commands, use the the Up arrow key to find
  previous commands and hit Enter to run them again. Instead of typing a
  modified command, use the Uu arrow to find a similar command, use text editing
  to modify that command and then hit Enter.


Viewing and manipulating the session parameters
-----------------------------------------------

Viewing and manipulating the :ref:`session parameters <session_parameters>`
used when performing operations against the :term:`DataONE` infrastructure
via the DataONE Command Line Interface (CLI).


Start the CLI::

  $ dataone.py

If desired, the session parameters can be reset back to their defaults (useful
if they were modified by an existing ``.d1client.conf`` file at startup)::

  > reset

Set some of the session parameters used by many of the operations when they
establish connections to :term:`MNs <MN>` and :term:`CNs <CN>`::

  > set cert-path /etc/dataone/client/certs/myclientcert.pem
  > set key-path /etc/dataone/client/certs/myclientcert.pem
  > set query *:*


Search results are returned as XML. Set the CLI to format XML to be more easily
readable by setting :ref:`pretty <pretty>` to **True**::

  > set pretty true

Include a restriction to only search for Science Data created at a specific
time or later::

  > set from-date 1998-01-01T05:00:00

View all the session parameters::

  > get

Save the session parameters to a file for later use::

  > save ~/d1/searchsettings

Exit the CLI::

  > exit



Searching for Science Data
--------------------------

A scientist can discover and download Science Data to leverage them in
their own research.

Start the CLI::

  $ dataone.py

Load the session parameters from the file created in the previous step::

  > load ~/d1/searchsettings

View the session parameters::

  > show

Modify the search parameters to find only Science Data that originated from
the "DEMO3" :term:`MN` and search again::

  > set query origin_mn:DEMO3
  > search

The search terms can also be specified after the "search" command::

  > search barnacle

Modify the search parameters to find only Science Data that are of type
text/csv and search again::

  > set format-id text/csv
  > search barnacle



Downloading Science Data Objects
--------------------------------

Start the CLI::

  $ dataone.py

View the session parameters::

  > show

Set :term:`MN` from which to download the Science Data Object::

  > set mn-url https://dataone.member.node.com/mn/

Download Science Data Object and save to local file::

  > get hdl:10255/dryad.669/mets.xml ~/my_dataone_files/dryad669.xml



Downloading System Metadata
---------------------------

System Metadata is an XML document that contains additional information about
a Science Data Object.

Start the CLI::

  $ dataone.py

Set the CLI to format XML to be more easily readable by setting :ref:`pretty
<pretty>` to **True**::

  > set pretty true

Retrieve the System Metadata and display it::

  > meta hdl:10255/dryad.669/mets.xml

Retrieve the System Metadata and save it to a file::

  > meta hdl:10255/dryad.669/mets.xml ~/d1/dryad669_system_metadata.xml



Uploading Science Data Objects
------------------------------

A scientist can upload a set of Science Data to benefit from the services
provided by DataONE.

Start the CLI::

  $ dataone.py

Select :term:`MN` to which to upload the Science Data Object::

  > set mn-url https://dataone.member.node.com/mn/

Configure the session parameters used when generating :term:`System Metadata`::

  > set submitter CN=MATTJTEMP,DC=dataone,DC=org
  > set rights-holder CN=MATTJTEMP,DC=dataone,DC=org
  > set origin-mn DEMO1
  > set authoritative-mn DEMO1

Create an Access Policy that has only public read permisisons::

  > denyall
  > allowpublic

Create (upload) the Science Data Object::

  > create mynewpid ~/path/to/my/file

Store the settings in ``.d1client.conf`` for use when creating similar
Science Data Objects later::

  > save

Exit the CLI::

  > exit



Misc operations
---------------

Find replicas of Science Data Objects::

  > resolve hdl:10255/dryad.669/mets.xml

Display list of Science Data Objects on a :term:`MN` or :term:`CN`::

  > set mn-url https://dataone.org/mn
  > set start 100
  > set count 10
  > list

Display event log on a :term:`MN`::

  > reset
  > set cert-path /etc/dataone/client/certs/myclientcert.pem
  > set key-path None
  > set mn-url https://dataone.org/mn
  > log

Download the event log and save it to a file::

  > log events.xml
