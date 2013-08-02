.. _`session_variables`:

Overview of session variables
=============================

========================= ========================= ======== ======================================================================================
Name                      Default                   Type     Description
========================= ========================= ======== ======================================================================================
**CLI configuration**
---------------------------------------------------------------------------------------------------------------------------------------------------
_`verbose`                False                     Boolean  Display more information
_`editor`                 nano                      String   Editor to use when editing the queue
------------------------- ------------------------- -------- --------------------------------------------------------------------------------------
**Target Nodes**
---------------------------------------------------------------------------------------------------------------------------------------------------
_`cn-url`                 https://cn.dataone.org/cn String   Node to which to connect for operations that access a DataONE Root :term:`CN`
_`mn-url`                 https://localhost/mn/     String   Node to which to connect for operations that access a DataONE :term:`MN`
------------------------- ------------------------- -------- --------------------------------------------------------------------------------------
**Authentication**
---------------------------------------------------------------------------------------------------------------------------------------------------
_`anonymous`              True                      Boolean  Ignore any installed certificates and connect anonymously
_`cert-file`              None                      String   Filesystem path to client certificate
_`key-file`               None                      String   Filesystem path to the client certificate private key. Not required if the certificate
                                                             provided with ``certpath`` contains both the public and private keys
------------------------- ------------------------- -------- --------------------------------------------------------------------------------------
**Slicing**
---------------------------------------------------------------------------------------------------------------------------------------------------
_`start`                  0                         Integer  First item to display for operations that display lists of items
_`count`                  1000                      Integer  Maximum number of items to display for operations that display lists of items
------------------------- ------------------------- -------- --------------------------------------------------------------------------------------
**Searching**
---------------------------------------------------------------------------------------------------------------------------------------------------
_`query`                  `*:*`                     String   Query string (SOLR or Lucene query syntax) for searches
_`query-type`             solr                      String   Select search engine (currently, only SOLR is available)
_`from-date`              None                      String   Start time used by operations that accept a time range
_`to-date`                None                      String   End time used by operations that accept a time range
_`search-format-id`       None                      String   Include only objects of this format
------------------------- ------------------------- -------- --------------------------------------------------------------------------------------
**Parameters | Misc**
---------------------------------------------------------------------------------------------------------------------------------------------------
_`algorithm`              SHA-1                     String   Checksum algorithm to use when calculating the checksum for a Science Data Object
_`format-id`              None                      String   ID for the Object Format to use when generating System Metadata
------------------------- ------------------------- -------- --------------------------------------------------------------------------------------
**Parameters | Reference Nodes**
---------------------------------------------------------------------------------------------------------------------------------------------------
_`authoritative-mn`       None                      String   Authoritative Member Node to use when generating System Metadata
_`origin-mn`              None                      String   Originating Member Node to use when generating System Metadata
------------------------- ------------------------- -------- --------------------------------------------------------------------------------------
**Parameters | Subjects**
---------------------------------------------------------------------------------------------------------------------------------------------------
_`rights-holder`          None                      String   Subject of the rights holder to use when generating System Metadata
_`submitter`              None                      String   Subject of the submitter to use when generating System Metadata
------------------------- ------------------------- -------- --------------------------------------------------------------------------------------
**Access Control**
---------------------------------------------------------------------------------------------------------------------------------------------------
Access Control Policy parameters managed by a :ref:`separate set of commands <access_policy>`.
---------------------------------------------------------------------------------------------------------------------------------------------------
**Replication**
---------------------------------------------------------------------------------------------------------------------------------------------------
Replication Policy parameters managed by a :ref:`separate set of commands <replication_policy>`.
===================================================================================================================================================
