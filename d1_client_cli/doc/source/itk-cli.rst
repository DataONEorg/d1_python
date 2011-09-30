DataONE Command Line Client (CLI)
=================================

Synopsis
--------

The DataONE command line client simplifies access to low level operations of
the DataONE infrastructure. 

Operation
---------

Basic syntax::

  dataone.py [parameters] operation arguments

Parameters
----------

  --dataone-url URL                         DataONE root
  --mn-url URL                              Member node
  --cn-url URL                              Coordinating node
  --cert-path CERT_FILE                     Filesystem path to client certificate
  --key-path KEY_FILE                       Filesystem path to the client certificate key
  --anonymous                               Ignore any installed certificates and connect anonymously
  --sysmeta-object-format FMTID             Specify the object format ID for system metadata
  --sysmeta-submitter S_SUBJECT             Specify the subject of the submitter in system metadata
  --sysmeta-rightsholder R_SUBJECT          Subject of the rights holder in system metadata  
  --sysmeta-origin-member-node O_MN         Set the origin member node identifier in the system metadata
  --sysmeta-authoritative-member-node A_MN  Set the authoritative member node identifier in the system metadata
  --sysmeta-access-policy                   Set the access policy to be stored in the system metadata
  --sysmeta-access-policy-public            If present, the system metadata will have public access policy
  --start-time STARTTIME                    The start time for operations that accept a time range
  --end-time ENDTIME                        The end time for operations that accept a time range
  --object-format FMTID                     Object format for requests
  --query QUERY                             Query string (SOLR_ or Lucene query syntax) for searches
  --fields FIELDS                           Comma delimited list of index fields to return in search responses
  --output FILE                             Store data to file instead of writing it to StdOut
  --pretty                                  Render Pretty Printed XML
  --verbose                                 Display more information
  --slice-start START                       Start position for sliced resultset
  --slice-count COUNT                       Max number of elements in sliced resultset
  --store-config                            Store config variables and exit. Configuration defaults are stored 
                                            in ``$HOME/.d1client.conf``


Operations
----------

create
~~~~~~

Add content to a member node::

  dataone.py --sysmeta-object-format FMTID 
            [--mn-url URL ] 
            [--sysmeta-submitter S_SUBJECT]
            [--sysmeta-rightsholder R_SUBJEC]
            [--sysmeta-origin-member-node O_MN]
            [--sysmeta-authoritative-member-node A_MN]
            [--sysmeta-access-policy-public]
            [--cert-path CERT_FILE]
            [--key-path KEY_FILE]
   create PID OBJECT_PATH


**Example**

::

  dataone.py --sysmeta-object-format text/csv \
    --sysmeta-submitter "CN=MATTJTEMP,DC=dataone,DC=org" \
    --sysmeta-rightsholder "CN=MATTJTEMP,DC=dataone,DC=org" \
    --sysmeta-origin-member-node DEMO1 \
    --sysmeta-authoritative-member-node DEMO1 \
    --mn-url https://demo1.test.dataone.org/knb/d1/mn/v1 \
    --cert-path /etc/dataone/client/certs/myclientcert.pem \
    --sysmeta-access-policy-public \
    create demo1.2.1 data/data-samples.csv


get
~~~

Retrieve content from a member or coordinating node::

  dataone.py [--dataone-url URL] 
             [--cert-path CERT_FILE]
             [--key-path KEY_FILE]
   get PID 

**Example**

::

  dataone.py --dataone-url https:/cn-dev.dataone.org/cn/v1 get demo3_3_2


meta
~~~~

Retrieve system metadata for an object

  dataone.py [--dataone-url URL] 
             [--cert-path CERT_FILE]
             [--key-path KEY_FILE]
   meta PID 

**Example**

::

  dataone.py --pretty --dataone-url https:/cn-dev.dataone.org/cn/v1 meta demo3_3_2


list 
~~~~

List objects on a member or coordinating node

  dataone.py [--mn-url URL] 
             [--cert-path CERT_FILE]
             [--key-path KEY_FILE]
             [--start-time STARTTIME] 
             [--end-time ENDTIME]
             [--object-format FMTID] 
             [--slice-start START] 
             [--slice-count COUNT]
             [--pretty]
   list 

**Example**

::

  dataone.py --anonymous \
             --mn-url=https://cn-dev.dataone.org/cn/v1 \
             --slice-count 10 \
             list


search
~~~~~~

Search system and science metadata indexed by a coordinating node::

  dataone.py [--cn-url URL] 
             [--query QUERY] 
             [--fields FIELDS] search 

**Examples**

Find objects with origin member node ID = "DEMO3"::

  dataone.py --cn_url="https://cn-dev.dataone.org/cn" --query "origin_mn:DEMO3" search
  
Find objects that contain the text "barnacle" anywhere in system or science metadata::

  dataone.py --cn_url="https://cn-dev.dataone.org/cn" --query "barnacle" search

Find objects of type "text/csv" that originated from member node ID = DEMO3

  dataone.py --cn-url="https://cn-dev.dataone.org/cn" \
             --query "origin_mn:DEMO3 AND objectformat:text/csv" search


Fields
~~~~~~

Return a list of fields available for search and retrieval from the
coordinating node index.

  dataone.py [--cn-url URL] fields

**Examples**

  dataone.py --cn-url="https://cn-dev.dataone.org/cn" fields



objectformats
~~~~~~~~~~~~~

Retrieve list of object formats

resolve
~~~~~~~

Retrieve location list for object.


log
~~~

Retrieve event logs





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

