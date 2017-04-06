Commands
========

.. contents::
  Table of Contents


Syntax
~~~~~~

``<...>`` denotes required arguments.

``[...]`` denotes optional arguments.

``file`` is the filesystem path to a local file.

Commands are case sensitive.


.. _commands_cli:

CLI
~~~

Commands that relate to the operation of the Command Line Interface itself.


.. _help:

help
----
Get help on commands

``help`` or ``?`` with no arguments displays a list of commands for which help is
available

``help <command>`` or ``? <command>`` gives help on <command>


.. _history:

history
-------
Display a list of commands that have been entered


.. _exit:

exit
----
Exit from the CLI


.. _quit:

exit
----
Exit from the CLI


.. _commands_session_general:

Session, General
~~~~~~~~~~~~~~~~

Commands that view and manipulate the session and the session variables.

.. _set:

set [variable [value]]
----------------------
``set (without parameters)``: Display the value of all session variables

``set <session variable>``: Display the value of a single session variable.

``set <session variable> <value>``: Set the value of a session variable.

See :ref:`access_policy` and :ref:`replication_policy` for information about how
to set the Access Policy and Replication Policy session variables.

An unset session variable has its value displayed as None. A session variable
can either be a Boolean (True / False), numeric or string value. See :ref:`set`
for more information on how to set session variables.


Also see :ref:`overview of session variables <session_variables>`.


.. _load:

load [file]
-----------
Load session variables from file

``load (without parameters)``: Load session from default file ``~/.dataone_cli.conf``

``load <file>``: Load session from specified file


.. _save:

save [config_file]
------------------
Save session variables to file

``save (without parameters)``: Save session to default file ``~/.dataone_cli.conf``

``save <file>``: Save session to specified file


.. _reset:

reset
-----
Set all session variables to their default values

The defaults are listed in the ``Default`` column in the :ref:`overview of
session variables <session_variables>`.


.. _commands_access_control:

Session, Access Control
~~~~~~~~~~~~~~~~~~~~~~~

The Access Policy is a list of subjects and their associated access levels. The
Access Policy is applied to new objects as they are :ref:`created <create>`. The
Access Policy can also be updated on existing Science Data Objects with
:ref:`updateaccess`.

Use the :ref:`set` command without any parameters to view the current Access
Policy.


.. _allowaccess:

allowaccess <subject> [access level]
------------------------------------
Set the access level for subject

Access level is ``read``, `write`` or ``changePermission``.

Access level defaults to ``read`` if not specified.

Special subjects:

  ``public``: Any subject, authenticated and not authenticated

  ``authenticatedUser``: Any subject that has authenticated with CILogon

  ``verifiedUser``: Any subject that has authenticated with CILogon and has been verified by DataONE

Any access level implicitly includes less permissive levels. E.g., giving
``changePermission`` to a subject implicitly gives ``read`` and ``write``
permissions as well.

To make objects accessible to the general public, give ``read`` access to the
public user. In some cases, it is desirable to obtain log records that include
information about who accessed a given object while still making the object
publicly accessible. This can be accomplished by giving ``read`` access only to
authenticatedUser. Access higher than ``read`` should not be given to any of the
special subjects.


.. _denyaccess:

denyaccess <subject>
--------------------
Remove subject from Access Policy.


.. _clearaccess:

clearaccess
-----------
Remove all subjects from Access Policy.

Only the submitter will have access to the object.



.. _commands_replication_policy:

Session, Replication Policy
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _allowrep:

allowrep
--------
Allow new objects to be replicated


.. _denyrep:

denyrep
-------
Prevent new objects from being replicated


.. _preferrep:

preferrep <member node> [member node ...]
-----------------------------------------
Add one or more preferred Member Nodes to replication policy


.. _blockrep:

blockrep <member node> [member node ...]
----------------------------------------
Add Member Node to list of blocked replication targets.


.. _removerep:

removerep <member node> [member node ...]
-----------------------------------------
Remove Member Node from list of preferred or blocked replication targets.


.. _numberrep:

numberrep <number of replicas>
------------------------------
Set preferred number of replicas for new objects

If the preferred number of replicas is set to zero, replication is also
disallowed.


.. _clearrep:

clearrep
--------
Set the replication policy to default

The default replication policy has no preferred or blocked member nodes, allows
replication and sets the preferred number of replicas to 3.


.. _commands_read_operations:

Read Operations
~~~~~~~~~~~~~~~

Commands that cause read operations to be issued against Coordinating Nodes and
Member Nodes.

Commands for retrieving :term:`Science Data Objects <Science Data
Object>`, :term:`System Metadata` and related information.


.. _get:

get <identifier> <file>
-----------------------
Get an object from a Member Node

The object is saved to ``file``.

Active session variables: :ref:`mn-url <mn-url>`, :ref:`authentication`


.. _meta:

meta <identifier> [file]
------------------------
Get the System Metadata that is associated with a Science Object

If the metadata is not on the Coordinating Node, the Member Node is checked.

Provide ``file`` to save the System Metada to disk instead of displaying it.

Active session variables: :ref:`cn-url <cn-url>`, :ref:`authentication`


.. _list:

list
----
Retrieve a list of available Science Data Objects from Member Node

The response is filtered by the from-date, to-date, search, start and count
session variables.

Active session variables: :ref:`mn-url <mn-url>`, :ref:`start <start>`,
:ref:`count <count>`, :ref:`from-date <from-date>`, :ref:`to-date <to-date>`,
:ref:`search-format-id <search-format-id>`, :ref:`authentication`

See also: :ref:`search`


.. _log:

log
---
Retrieve event log from Member Node

The response is filtered by the from-date, to-date, start and count session
parameters.

Active session variables: :ref:`mn-url <mn-url>`, :ref:`start <start>`,
:ref:`count <count>`, :ref:`from-date <from-date>`, :ref:`to-date <to-date>`,
:ref:`search-format-id <search-format-id>`, :ref:`authentication`


.. _resolve:

resolve <:term:`pid`>
---------------------
Find all locations from which the given Science Object can be downloaded.

Active session variables: :ref:`cn-url <cn-url>`, :ref:`authentication`


.. _commands_write_operations:

Write Operations
~~~~~~~~~~~~~~~~

Commands that cause write operations to be issued against Coordinating Nodes and
Member Nodes.

.. _create:

create <:term:`pid`> <file>
---------------------------
Create a new Science Object on a Member Node.

The System Metadata that becomes associated with the new Science Object is
generated from the session variables.

The algorithm set in :ref:`algorithm <algorithm>` is used for calculating the checksum
for the new object. If the value is unset, it defaults to the DataONE system
wide default, which is currently SHA1.

Active session variables: :ref:`mn-url <mn-url>`, :ref:`format-id
<format-id>`, :ref:`submitter <submitter>`, :ref:`rights-holder
<rights-holder>`, :ref:`origin-mn <origin-mn>`, :ref:`authoritative-mn
<authoritative-mn>`, :ref:`algorithm <algorithm>`, :ref:`access_policy`,
:ref:`replication_policy`, :ref:`authentication`


.. _update:

update <old-pid> <new-pid> <file>
---------------------------------
Replace an existing Science Object in a :term:`MN` with another.

The existing Science Object becomes obsoleted by the new Science Object.
obsoleted by the new values in the :ref:`System Metadata <session_variables>`,
:ref:`access_policy` and :ref:`replication_policy` session variables.

The algorithm set in :ref:`algorithm <algorithm>` is used for calculating the
checksum for the new object. If the value is unset, it defaults to the DataONE
system wide default, which is currently SHA1.

Active session variables: :ref:`mn-url <mn-url>`, :ref:`format-id <format-id>`,
:ref:`submitter <submitter>`, :ref:`rights-holder <rights-holder>`,
:ref:`origin-mn <origin-mn>`, :ref:`authoritative-mn <authoritative-mn>`,
:ref:`algorithm <algorithm>`, :ref:`access_policy`, :ref:`replication_policy`,
:ref:`authentication`


.. _package:

package <package-pid> <science-metadata-pid> <science-pid> [science-pid ...]
----------------------------------------------------------------------------
Create a simple :term:`OAI-ORE` Resource Map on a Member Node


.. _archive:

archive <identifier> [identifier ...]
-------------------------------------
Mark one or more existing Science Objects as archived


.. _updateaccess:

updateaccess <identifier> [identifier ...]
------------------------------------------
Update the Access Policy on one or more existing Science Data Objects

Requires that the calling subject has :ref:`authenticated <Authentication>` and
has changePermission access level on the object for which Access Policy is to be
updated.

Active session variables: :ref:`cn-url <cn-url>`, :ref:`authentication`,
:ref:`access_policy`


.. _updatereplication:

updatereplication <identifier> [identifier ...]
-----------------------------------------------
Update the Replication Policy on one or more existing Science Data Objects

Requires that the calling subject has :ref:`authenticated <Authentication>` and
has changePermission access level on the object for which Replication Policy is
to be updated.

Active session variables: :ref:`cn-url <cn-url>`, :ref:`replication_policy`,
:ref:`authentication`


.. _commands_utilities:

Utilities
~~~~~~~~~

.. _listformats:

listformats
-----------
Display all known Object Format IDs


.. _listnodes:

listnodes
---------
Display all known DataONE Nodes

.. _search_query:

search [query]
Comprehensive search for Science Data Objects across all available MNs

See https://releases.dataone.org/online/api-documentation-v2.0.1/design/SearchMetadata.html
for the available search terms.

.. _ping:

ping [base-url ...]
-------------------
Check if a server responds to the DataONE ping() API method ping (no arguments):
Ping the CN and MN that is specified in the session ping <base-url> [base-url
...]: Ping each CN or MN

If an incomplete base-url is provided, default CN and MN base URLs at the given
url are pinged.


.. _commands_write_operation_queue:

Write Operation Queue
~~~~~~~~~~~~~~~~~~~~~

Commands that view and manipulate the write operation queue.

.. _queue:

queue
-----
Print the queue of write operations.

.. _run:

run
---
Perform each operation in the queue of write operations


.. _edit:

edit
----
Edit the queue of write operations


.. _clearqueue:

clearqueue
----------
Remove the operations in the queue of write operations without performing them


