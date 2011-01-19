DataONE Command Line Client (CLI)
=================================

Synopsis
--------

The DataONE Command Line Client provides easy access to basic operations against
the DataONE infrastructure. The operations include:

* **create**: Create a Science Objects
* **get**: Retrieve Science Objects
* **meta**: Retrieve DataONE System Metadata related to Science Objects
* **related**: Discover relationships between Science Objects
* **list**: List Science Objects on Member Nodes
* **search**: Search for Science Objects on Coordinating Nodes
* **log**: Retrieve event logs
* **objectformats**: Retrieve list of object formats
* **resolve**: Retrieve location list for object.

User stories 
------------

* A scientist can upload a set of Science Objects to benefit from the services
  provided by DataONE.

* A scientist can discover and download Science Objects to leverage them in
  their own research.

* A scientist can discover relationships between Science Metadata and Science
  Data.


Usage Examples
--------------

create
~~~~~~

Upload a Science Data object and a related Science Metadata object to DataONE
and specify an identifier.

Example::

  $ ./dataone.py create my_identifier ./sysmeta/my_sysmeta.xml
  ./scimeta/my_scimeta.xml ./scidata/my_scidata.csv


get
~~~

Download a Science Object by its identifier::

  $ ./dataone.py get my_identifier


Download a Science Object by its identifier, storing the object in a file instead
of displaying it on screen::

  $ ./dataone.py get my_identifier --output="./my_file"

meta
~~~~

Download the DataONE System Metadata for a Science Object::

  $ ./dataone.py meta my_identifier

Download the DataONE System Metadata for a Science Object, formatted for human
reading::

  $ ./dataone.py meta my_identifier --pretty


related
~~~~~~~

Find Science Objects related to a given Science Object by identifier::

  $ ./dataone.py related my_identifier


list
~~~~

Download a list of the Science Objects stored on a given Member Node. The number
of Objects in the list is limited to 1000 by default::

  $ ./dataone.py list --mn-url=http://mn.invalid.com/mn

Download a list of the first 100 Science Objects stored on a given Member Node::

  $ ./dataone.py list --mn-url=http://mn.invalid.com/mn --slice-count=100

Download a list of the first 100 Science Objects stored on a given Member Node.
Store the list to a file instead of displaying it on screen::

  $ ./dataone.py list --mn-url=http://mn.invalid.com/mn --slice-count=100
  --output=my_list.xml

Download a list of 100 Science Objects stored on a given Member Node, starting
at the 100th object::

  $ ./dataone.py list --mn-url=http://mn.invalid.com/mn --slice-start=100
  --slice-count=100

Download a list of 100 Science Objects stored on a given Member Node, starting
at the 100th object. Format the list for human reading::

  $ ./dataone.py list --mn-url=http://mn.invalid.com/mn --slice-start=100
  --slice-count=100 --pretty

Download a list of the first 100 Science Objects stored on a given Member Node,
that were created in 2005::

  $ ./dataone.py list --mn-url=http://mn.invalid.com/mn --slice-count=100
  --start-time=2005-01-01 --end-time=2006-01-01.

Download a list of the first 100 Science Objects of a given format stored on a
given Member Node::

  $ ./dataone.py list --mn-url=http://mn.invalid.com/mn --slice-count=100
  --object-format="my_format_string"


search
~~~~~~

Search for Science Objects in the DataONE infrastructure matching an identifier
that starts with "abc". Format the result for human reading::

  $ ./dataone.py search "abc*" --pretty
  
Filter the search results for a given time period, format for human reading and
store in a file::

  $ ./dataone.py search "abc*" --pretty --output="./my_file"
  --start-time=2010-01-01T05:00:00 --end-time=2010-01-01T06:00:00


log
~~~

Retrieve logs related to a given identifier::

  $ ./dataone.py log "abc*"
  
Retrieve logs related to a given identifier, filtered by event type, formatted
for human reading::
  
  $ ./dataone.py log "abc*" --event-type=read --pretty

Valid event types::

  create, read, update, delete, replicate
  

objectformats
~~~~~~~~~~~~~

Retrieve list of object formats::

  $ ./dataone.py objectformats
  
resolve
~~~~~~~

Retrieve location list for object::

  $ ./dataone.py resolve my_identifier

