.. _science_object_operations:

Science Object Operations
-------------------------

Commands for creating and retrieving :term:`Science Data Objects <Science Data
Object>` and :term:`System Metadata`.


.. _getdata:

getdata <:term:`pid`> <file>
````````````````````````````
Get a Science Data Object from a :term:`MN`.

The Science Object is saved to ``file``.

Active session parameters: :ref:`mnurl <mnurl>`, :ref:`authentication`


.. _meta:

meta <:term:`pid`> [file]
`````````````````````````
Get the System Metadata that is associated with a Science Object from a
:term:`CN`.

Provide ``file`` if saving the System Metadata is desired.

Connects to the :term:`CN` set in the :ref:`dataoneurl <dataoneurl>` session
parameter.

Active session parameters: :ref:`dataoneurl <dataoneurl>`, :ref:`authentication`


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

Active session parameters: :ref:`mnurl <mnurl>`, :ref:`objectformat
<objectformat>`, :ref:`submitter <submitter>`, :ref:`rightsholder
<rightsholder>`, :ref:`originmn <originmn>`, :ref:`authoritativemn
<authoritativemn>`, :ref:`algorithm <algorithm>`, :ref:`access_policy`,
:ref:`replication_policy`, :ref:`authentication`


.. _related:

related <:term:`pid`>
`````````````````````
Given the :term:`pid` for a Science Data Object, find it's Science Metadata and
vice versa.

Provide ``file`` if saving the information is desired.

Connects to the :term:`CN` set with the **dataone_url** session
parameter.

Active session parameters: :ref:`dataoneurl <dataoneurl>`, :ref:`authentication`


.. _resolve:

resolve <:term:`pid`>
`````````````````````
Given the :term:`pid` for a Science Object, find all locations from which the
Science Object can be downloaded.

Active session parameters: :ref:`dataoneurl <dataoneurl>`, :ref:`authentication`


.. _list:

list
````
Retrieve a list of available Science Data Objects from a single :term:`MN` with
basic filtering.

Active session parameters: :ref:`mnurl <mnurl>`, :ref:`start <start>`,
:ref:`count <count>`, :ref:`fromdate <fromdate>`, :ref:`todate <todate>`,
:ref:`searchobjectformat <searchobjectformat>`, :ref:`authentication`

See also: :ref:`search`


.. _log:

log
```
Retrieve event log for a Science Object.

Active session parameters: :ref:`mnurl <mnurl>`, :ref:`start <start>`,
:ref:`count <count>`, :ref:`fromdate <fromdate>`, :ref:`todate <todate>`,
:ref:`searchobjectformat <searchobjectformat>`, :ref:`authentication`


.. _setaccess:

setaccess <:term:`pid`>
```````````````````````
Update the Access Policy on an existing Science Data Object.

Requires that the calling subject has :ref:`authenticated <Authentication>` and
has changePermission access level on the object for which Access Policy is to be
updated.

Active session parameters: :ref:`dataoneurl <dataoneurl>`,
:ref:`authentication`, :ref:`access_policy`


.. _setreplication:

setreplication <:term:`pid`>
````````````````````````````
Update the Replication Policy on an existing Science Data Object.

Requires that the calling subject has :ref:`authenticated <Authentication>` and
has changePermission access level on the object for which Replication Policy is
to be updated.

Active session parameters: :ref:`dataoneurl <dataoneurl>`,
:ref:`replication_policy`, :ref:`authentication`
