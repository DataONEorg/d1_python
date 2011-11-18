Reference
=========

.. _session_parameters_intro:

Session parameters
~~~~~~~~~~~~~~~~~~

Various operations can be performed against the :term:`DataONE` infrastructure
via the DataONE Command Line Interface (CLI). The operations obtain the
parameters they require from a set of shared, configurable, values called
session parameters. An :ref:`overview of session parameters
<session_parameters>` is available below.


Startup
~~~~~~~

When the CLI starts, it attempts to load the session parameters from a
configuration file named ``.d1client.conf``, located in the user's home
directory. If the configuration file is not present, the session parameters are
set to default values as shown in the ``Default`` column in the :ref:`overview
of session parameters <session_parameters>`.

The CLI then executes any commands specified on the command line, in the
specified order. This includes any :ref:`set <set>` commands that modify the
session parameters.


.. _command_line_arguments:

Command line arguments
~~~~~~~~~~~~~~~~~~~~~~

One or more commands may be specified on the command line. The CLI will execute
these before entering interactive mode. The CLI can be prevented from entering
interactive mode by adding the :ref:`exit` command to the end of the list of
commands.

E.g., the following command will start the CLI, execute a :ref:`list` command
based on any default values in the ``.d1client.conf`` file and then :ref:`exit`.

::

  $ dataone.py list exit

Commands that contain spaces or other symbols that have specific meaning to the
shell must be quoted with single quotes::

  $ dataone.py 'get mypid myfile'

The session parameters available in interactive mode can be modified on startup
by specifying :ref:`set <set>` commands. E.g., the following is the same as
first running ``dataone.py`` and then typing the two commands, ``set start 100``
and ``set count 10``::

  $ dataone.py 'set start 100' 'set count 10'


Commands
~~~~~~~~

``[...]`` denotes optional arguments.

``<...>`` denotes required arguments.

``file`` is the full filesystem path to a local file.

Commands are case sensitive.


Session parameters management
-----------------------------

Commands to view and manipulate the :ref:`session parameters
<session_parameters_intro>`.

Session parameters can be set to their default values with :ref:`reset`.

Session parameters can be stored in files for reuse with :ref:`load <load>` and
:ref:`save <save>`. When these commands are issued without filenames, they
default to using the ``.d1client.conf`` file, located in the user's home
directory.

The full set of session parameters can be displayed with :ref:`get <get>` and
individual parameters can be displayed with :ref:`get`.

Most of the session parameters are modified with :ref:`set <set>`. The session
parameters also contain an access control list. The access control list is
manipulated with a :ref:`separate set of commands <access_policy>`.

An unset session parameter has its value displayed as None. A session parameter
can either be a Boolean (True / False), numeric or string value. See :ref:`set
<set>` for more information on how to set session parameters.

In the following commands, ``session parameter`` is a parameter name taken from
the ``Name`` column in the :ref:`overview of session parameters
<session_parameters>`.


.. _reset:

reset
`````
Set all session parameters to their default values, listed in the ``Default``
column in the :ref:`overview of session parameters <session_parameters>`.


.. _load:

load [file]
```````````
Load session parameters from file. If ``file`` is not provided, defaults to
``.d1client.conf``, located in the user's home directory.


.. _save:

save [file]
```````````
Save session parameters to file. If ``file`` is not provided, defaults to
``.d1client.conf``, located in the user's home directory.


.. _get:

get [session parameter]
```````````````````````
Display the value of a session parameter. If ``session parameter`` is not
provided, display all session parameters.


.. _set:

set <session parameter> <value>
```````````````````````````````
Set the value of a session parameter.


.. _clear:

clear <session parameter>
`````````````````````````
Clear the value of a session parameter.


.. _access_policy:

Access Policy
-------------

The Access Policy is a list of subjects with associated access levels. The
Access Policy is automatically applied to new objects as they are :ref:`created
<create>`. The Access Policy can also be updated on existing Science Data
Objects with :ref:`setaccess <setaccess>`.

Commands to view and manipulate the access policy that is applied to newly
created objects.


.. _allow:

allow <subject> [access level]
``````````````````````````````
Allow access to ``subject``. If ``access level`` is not provided, it defaults to
**read**. Valid access levels are: read, write, changePermission, execute and
replicate. Any access level implicitly includes less permissive levels. E.g.,
giving changePermission to a subject implicitly gives read and write permissions
as well.


.. _deny:

deny <subject>
``````````````
Remove subject from access policy.


.. _allowpublic:

allowpublic
```````````
Allow public read.


.. _denypublic:

denypublic
``````````
Deny public read.


.. _denyall:

denyall
```````
Remove all subjects from access policy and deny public read. Only the submitter
will have access to the object.


.. _authentication:

Authentication
--------------

A user that accesses a :term:`CN` or :term:`MN` may connect as an authenticated
subject or anonymously.

The CN or MN to which the user connects will allow access only to operations,
Science Objects and other data to which permissions have been granted for the
subject with which the user has authenticated.

A user that connects anonymously is granted access only to publicly available
operations and data. Access is typically denied for operations that create or
modify data, such as the :ref:`create <create>` operation.

When the CLI connects to a CN or MN on a user's behalf, it passes authentication
information for that user via a :term:`certificate`. The certificate enables the
user to act as a specific subject within a CN or MN.

The user obtains a certificate for the subject with which to access a CN or MN
from :term:`CILogon`. When the user downloads a certificate from CILogon, the
CILogon download process stores the certificate in a standard location. The CLI
can automatically find certificates in this location. In some cases,
certificates may be stored in custom locations. In such cases, the automatic
location of certificates can be bypassed by setting the `cert-path`_ session
parameter to the filesystem path of the certificate. Because CILogon provides a
certificate that holds both the public and private keys in the same file, only
`cert-path`_ is required and `key-path`_ should be set to None. If the
certificate was obtained in some other way, and the certificate's private key is
stored in a separate file, the `key-path`_ session parameter must be set to the
filesystem path of the private key.

When a user types a command that requires the CLI to connect to a CN or MN, the
CLI starts by examining the value of the the `anonymous`_ session parameter. If
the `anonymous`_ session parameter is **True**, the CLI ignores any available
certificate and connects to the DataONE CN or MN without providing a
certificate. This causes the CN or MN to allow access only to publicly available
operations and data.

If the `anonymous`_ session parameter is **False**, the CLI attempts to locate
the user's certificate as described above. If a certificate is not found, the
operation is aborted. If a certificate is found, the CLI passes the certificate
to the CN or MN when establishing the connection. The CN or MN validates the
certificate and may reject it, causing the operation to be aborted. If the
certificate is successfully validated, the CN or MN grants access to the user,
authenticated as the subject designated in the certificate, and the CLI proceeds
with the operation.



.. _science_object_operations:

Science Object Operations
-------------------------

Commands for creating and retrieving :term:`Science Data Objects <Science Data
Object>` and :term:`System Metadata`.

.. _create:

create <:term:`pid`> <file>
```````````````````````````
Create a new Science Object on a :term:`MN`.

The System Metadata that becomes associated with the new Science Object is
automatically generated from the values in the :ref:`System Metadata
<session_parameters>` section in the session parameters and the
:ref:`access_policy`.

The algorithm set in `algorithm`_ is used for calculating the checksum
for the new object. If the value is unset, it defaults to the DataONE system
wide default, which is currently SHA1.

Active session parameters: `pretty`_, `verbose`_, `mn-url`_, `cert-path`_,
`key-path`_, `object-format`_, `submitter`_, `rightsholder`_, `origin-mn`_,
`authoritative-mn`_, `algorithm`_, :ref:`access_policy`


.. _getdata:

getdata <:term:`pid`> <file>
````````````````````````````
Get a Science Data Object from a :term:`MN`.

The Science Object is saved to ``file``.

Active session parameters: `pretty`_, `verbose`_, `mn-url`_, `anonymous`_,
`cert-path`_, `key-path`_


.. _meta:

meta <:term:`pid`> [file]
`````````````````````````
Get the System Metadata that is associated with a Science Object from a
:term:`CN`.

Provide ``file`` if saving the System Metadata is desired.

Connects to the :term:`CN` set in the **dataone_url** session
parameter.

Active session parameters: `pretty`_, `verbose`_, `mn-url`_, `anonymous`_,
`cert-path`_, `key-path`_


.. _setaccess:

setaccess <:term:`pid`>
```````````````````````
Update the Access Policy on an existing Science Data Object.

Requires that the calling subject has changePermission access level on the
object for which access policy is to be updated. Because the public subject can
not have any access level higher than **read**, this command will not work
unless the ``public`` session parameter is set to false and a valid certificate
is available in the standard location or has been set up with the **cert-path**
session parameter (and optionally, the **key-path** parameter.)

Active session parameters: `pretty`_, `verbose`_, `dataone-url`_, `cert-path`_,
`key-path`_, :ref:`access_policy`


.. _related:

related <:term:`pid`>
`````````````````````
Given the :term:`pid` for a Science Data Object, find it's Science Metadata and
vice versa.

Provide ``file`` if saving the information is desired.

Connects to the :term:`CN` set with the **dataone_url** session
parameter.

Active session parameters: `pretty`_, `verbose`_, `dataone-url`_, `anonymous`_,
`cert-path`_, `key-path`_


.. _resolve:

resolve <:term:`pid`>
`````````````````````
Given the :term:`pid` for a Science Object, find all locations from which the
Science Object can be downloaded.

Active session parameters: `pretty`_, `verbose`_, `dataone-url`_, `anonymous`_,
`cert-path`_, `key-path`_


.. _list:

list
````
Retrieve a list of available Science Data Objects from a single :term:`MN` with
basic filtering.

Active session parameters: mn-url_, cert-path_, key-path_, start-time_,
end-time_, object-format_, start_, count_, pretty_

Active session parameters: `pretty`_, `verbose`_, `mn-url`_, `start`_, `count`_,
`anonymous`_, `cert-path`_, `key-path`_, `start-time`_, `end-time`_,
`search-object-format`_,

See also: :ref:`search`


.. _log:

log
```
Retrieve event log for a Science Object.

Active session parameters: `pretty`_, `verbose`_, `mn-url`_, `start`_, `count`_,
`anonymous`_, `cert-path`_, `key-path`_, `start-time`_, `end-time`_,
`search-object-format`_,


Searching
---------

.. _search:

search
``````
Comprehensive search for Science Data Objects across all available :term:`MNs
<MN>`.

Active session parameters: `pretty`_, `verbose`_, `dataone-url`_, `start`_,
`count`_, `anonymous`_, `cert-path`_, `key-path`_, `start-time`_, `end-time`_,
`search-object-format`_, `query`_, `fields`_


.. _fields_command:

fields
``````
List the SOLR index fields that are available for use in :ref:`search`.

Active session parameters: `pretty`_, `verbose`_, `dataone-url`_


CLI
---

Commands that relate to the operation of the Command Line Interface itself.


.. _history:

history
```````
Display a list of commands that have been entered.


.. _exit:

exit
````
Exit from the CLI.


.. _help:

help
````
Get help on commands.

``help`` or ``?`` with no arguments displays a list of commands for which help is
available.

``help <command>`` or ``? <command>`` gives help on <command>.


.. _verbose_header:

Verbose
```````
The CLI can be set to display more information as operations are performed by
turning the `verbose`_ session variable to True.


.. _xml_formatting:

XML formatting
``````````````
Some commands display XML. The CLI can be set to format XML to be more easily
readable by setting `pretty`_ to True.


.. _`session_parameters`:

Overview of session parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

========================= ===================== ======== ======================================================================================
Name                      Default               Type     Description
========================= ===================== ======== ======================================================================================
**CLI configuration**
-----------------------------------------------------------------------------------------------------------------------------------------------
_`pretty`                 True                  Boolean  Display XML with human friendly formatting
_`verbose`                False                 Boolean  Display more information
------------------------- --------------------- -------- --------------------------------------------------------------------------------------
**Node selection**
-----------------------------------------------------------------------------------------------------------------------------------------------
_`dataone-url`            SYSTEM DEFAULT        String   Node to which to connect for operations that access the DataONE Root :term:`CN`
_`mn-url`                 https://localhost/mn/ String   Node to connect to for operations that access a DataONE :term:`MN`
------------------------- --------------------- -------- --------------------------------------------------------------------------------------
**Slicing**
-----------------------------------------------------------------------------------------------------------------------------------------------
_`start`                  0                     Integer  First item to display for operations that display lists of items
_`count`                  SYSTEM DEFAULT        Integer  Maximum number of items to display for operations that display lists of items
------------------------- --------------------- -------- --------------------------------------------------------------------------------------
**Authentication**
-----------------------------------------------------------------------------------------------------------------------------------------------
_`anonymous`              False                 Boolean  Ignore any installed certificates and connect anonymously.
_`cert-path`              None                  String   Filesystem path to client certificate
_`key-path`               None                  String   Filesystem path to the client certificate private key. Not required if the certificate
                                                         provided with ``cert-path`` contains both the public and private keys
------------------------- --------------------- -------- --------------------------------------------------------------------------------------
**System Metadata**
-----------------------------------------------------------------------------------------------------------------------------------------------
_`object-format`          None                  String   ID for the Object Format to use when generating System Metadata
_`submitter`              None                  String   Subject of the submitter to use when generating System Metadata
_`rightsholder`           None                  String   Subject of the rights holder to use when generating System Metadata
_`origin-mn`              None                  String   Originating Member node to use when generating System Metadata
_`authoritative-mn`       None                  String   Authoritative :term:`MN` to use when generating System Metadata
_`algorithm`              SYSTEM DEFAULT        String   Checksum algorithm to use when calculating the checksum for a Science Data Object
------------------------- --------------------- -------- --------------------------------------------------------------------------------------
**Search**
-----------------------------------------------------------------------------------------------------------------------------------------------
_`start-time`             None                  String   Start time used by operations that accept a time range
_`end-time`               None                  String   End time used by operations that accept a time range
_`search-object-format`   None                  String   Include only objects of this format
_`query`                  `*:*`                 String   Query string (SOLR or Lucene query syntax) for searches
_`fields`                 None                  String   Comma delimited list of index fields to return in search responses
========================= ===================== ======== ======================================================================================
