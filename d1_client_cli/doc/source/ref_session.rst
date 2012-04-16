Session parameters
------------------

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


.. show:

show [session parameter]
````````````````````````
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
_`anonymous`              True                  Boolean  Ignore any installed certificates and connect anonymously
_`cert-path`              None                  String   Filesystem path to client certificate
_`key-path`               None                  String   Filesystem path to the client certificate private key. Not required if the certificate
                                                         provided with ``certpath`` contains both the public and private keys
------------------------- --------------------- -------- --------------------------------------------------------------------------------------
**System Metadata**
-----------------------------------------------------------------------------------------------------------------------------------------------
_`algorithm`              SYSTEM DEFAULT        String   Checksum algorithm to use when calculating the checksum for a Science Data Object
_`authoritative-mn`       None                  String   Authoritative Member Node to use when generating System Metadata
_`origin-mn`              None                  String   Originating Member Node to use when generating System Metadata
_`format-id`              None                  String   ID for the Object Format to use when generating System Metadata
_`rights-holder`          None                  String   Subject of the rights holder to use when generating System Metadata
_`submitter`              None                  String   Subject of the submitter to use when generating System Metadata
------------------------- --------------------- -------- --------------------------------------------------------------------------------------
**Search**
-----------------------------------------------------------------------------------------------------------------------------------------------
_`from-date`              None                  String   Start time used by operations that accept a time range
_`to-date`                None                  String   End time used by operations that accept a time range
_`search-format-id`       None                  String   Include only objects of this format
_`query`                  `*:*`                 String   Query string (SOLR or Lucene query syntax) for searches
_`query-type`             solr                  String   Select search engine (currently, only SOLR is available)
------------------------- --------------------- -------- --------------------------------------------------------------------------------------
**Access Policy**
-----------------------------------------------------------------------------------------------------------------------------------------------
Parameters managed by a :ref:`separate set of commands <access_policy>`.
-----------------------------------------------------------------------------------------------------------------------------------------------
**Replication Policy**
-----------------------------------------------------------------------------------------------------------------------------------------------
Parameters managed by a :ref:`separate set of commands <replication_policy>`.
===============================================================================================================================================
