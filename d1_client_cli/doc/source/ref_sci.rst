.. _science_object_operations:

Science Object Operations
-------------------------

Commands for creating and retrieving :term:`Science Data Objects <Science Data
Object>` and :term:`System Metadata`.


.. _get:

get <:term:`pid`> <file>
````````````````````````````
Get an object from a :term:`MN`.

The object is saved to ``file``.

Active session parameters: :ref:`mn-url <mn-url>`, :ref:`authentication`


.. _meta:

meta <:term:`pid`> [file]
`````````````````````````
Get the System Metadata that is associated with a Science Object from a
:term:`CN`.

Provide ``file`` if saving the System Metadata is desired.

Connects to the :term:`CN` set in the :ref:`dataone-url <dataone-url>` session
parameter.

Active session parameters: :ref:`dataone-url <dataone-url>`, :ref:`authentication`


.. _create:

create <:term:`pid`> <file>
```````````````````````````
Create a new Science Object on a :term:`MN`.

The System Metadata that becomes associated with the new Science Object is
generated from the values in the :ref:`System Metadata <session_parameters>`,
:ref:`access_policy` and :ref:`replication_policy` session parameters.

The algorithm set in :ref:`algorithm <algorithm>` is used for calculating the checksum
for the new object. If the value is unset, it defaults to the DataONE system
wide default, which is currently SHA1.

Active session parameters: :ref:`mn-url <mn-url>`, :ref:`format-id
<format-id>`, :ref:`submitter <submitter>`, :ref:`rights-holder
<rights-holder>`, :ref:`origin-mn <origin-mn>`, :ref:`authoritative-mn
<authoritative-mn>`, :ref:`algorithm <algorithm>`, :ref:`access_policy`,
:ref:`replication_policy`, :ref:`authentication`


.. _update:

update <:term:`pid`> <file> <:term:`pid`>
`````````````````````````````````````````
Replace an existing Science Object in a :term:`MN` with another.

The existing Science Object becomes obsoleted by the new Science Object.
obsoleted by the new values in the :ref:`System Metadata <session_parameters>`,
:ref:`access_policy` and :ref:`replication_policy` session parameters.

The algorithm set in :ref:`algorithm <algorithm>` is used for calculating the checksum
for the new object. If the value is unset, it defaults to the DataONE system
wide default, which is currently SHA1.

Active session parameters: :ref:`mn-url <mn-url>`, :ref:`format-id
<format-id>`, :ref:`submitter <submitter>`, :ref:`rights-holder
<rights-holder>`, :ref:`origin-mn <origin-mn>`, :ref:`authoritative-mn
<authoritative-mn>`, :ref:`algorithm <algorithm>`, :ref:`access_policy`,
:ref:`replication_policy`, :ref:`authentication`


.. _delete:

delete <:term:`pid`>
````````````````````
Mark an existing Science Object as archived.

Active session parameters: :ref:`mn-url <mn-url>`, :ref:`submitter <submitter>`,
:ref:`access_policy`, :ref:`replication_policy`, :ref:`authentication`


.. _resolve:

resolve <:term:`pid`>
`````````````````````
Given the :term:`pid` for a Science Object, find all locations from which the
Science Object can be downloaded.

Active session parameters: :ref:`dataone-url <dataone-url>`, :ref:`authentication`


.. _list:

list
````
Retrieve a list of available Science Data Objects from a single :term:`MN` with
basic filtering.

Active session parameters: :ref:`mn-url <mn-url>`, :ref:`start <start>`,
:ref:`count <count>`, :ref:`from-date <from-date>`, :ref:`to-date <to-date>`,
:ref:`search-format-id <search-format-id>`, :ref:`authentication`

See also: :ref:`search`


.. _log:

log
```
Retrieve event log.

Active session parameters: :ref:`mn-url <mn-url>`, :ref:`start <start>`,
:ref:`count <count>`, :ref:`from-date <from-date>`, :ref:`to-date <to-date>`,
:ref:`search-format-id <search-format-id>`, :ref:`authentication`


.. _setaccess:

setaccess <:term:`pid`>
```````````````````````
Update the Access Policy on an existing Science Data Object.

Requires that the calling subject has :ref:`authenticated <Authentication>` and
has changePermission access level on the object for which Access Policy is to be
updated.

Active session parameters: :ref:`dataone-url <dataone-url>`,
:ref:`authentication`, :ref:`access_policy`


.. _setreplication:

setreplication <:term:`pid`>
````````````````````````````
Update the Replication Policy on an existing Science Data Object.

Requires that the calling subject has :ref:`authenticated <Authentication>` and
has changePermission access level on the object for which Replication Policy is
to be updated.

Active session parameters: :ref:`dataone-url <dataone-url>`,
:ref:`replication_policy`, :ref:`authentication`
