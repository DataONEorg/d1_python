.. _data_package:

Data packages
=============

DataONE supports a system that allows relationships between DataONE science
objects to be described. These relationships are stored in :term:`OAI-ORE Resource
Map`\s.

This module provides functionality for the most common use cases when
parsing and generating Resource Maps for use in DataONE.

See `Data Packaging
<https://releases.dataone.org/online/api-documentation-v2.0.1/design/DataPackage.html>`_
for more information about how Resource Maps are used in DataONE.


ResourceMapGenerator
~~~~~~~~~~~~~~~~~~~~

Generate an OAI-ORE resource map for the common scenario where one
resource map describes an aggregation containing a single Science Metadata
object and one or more Science Data objects described by that object.

Generate a system metadata object for a resource map. The generated
system metadata object is intended for use in DataONE API methods such as
MNStorage.Create(). The object contains an access control rule allowing
public access. For simple use cases with public access, the object can
often be used as is. For more complex use cases, the object can be modified
programmatically before use.



ResourceMapParser
~~~~~~~~~~~~~~~~~

Parse a string containing a OAI-ORE document in RDF-XML and provide convenient
access to information required by many DataONE clients, such as lists of
aggregated science data and science metadata identifiers.

