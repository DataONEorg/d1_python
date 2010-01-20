'''
Module pyd1.d1const
===================

:Created: 20100111
:Author: vieglais

Provides various constants for the PyD1 client.
'''

#: :const: Version of this software
VERSION = "0.0.0"

#: types of objects in the DataONE system
OBJECT_CLASSES = ['data', 'metadata', 'system']

#: Maximum number of entries per list objects request
MAX_LISTOBJECTS = 1000

#: Default number of objects to retrieve in a list objects request
DEFAULT_LISTOBJECTS = 100

#: HTTP Response timeout in seconds, float.
RESPONSE_TIMEOUT = 30.0

#: HTTP User Agent that this software is known as
USER_AGENT = 'pyd1/%s +http://dataone.org/' % VERSION

#: The root of all DataONE.  Used to perform introspection on the system when
#: no other node information is provided.
URL_DATAONE_ROOT = "http://cn.dataone.org/"

#: Path to append to target base for the object collection
URL_OBJECT_PATH = 'object'

#: Path to append to target base for system metadata collection
URL_SYSMETA_PATH = 'meta'

#: Path to the DataONE system metadata schema
SYSTEM_METADATA_SCHEMA_URL = "https://repository.dataone.org/software/cicore/"+\
                             "trunk/schemas/coordinating_node_sysmeta.xsd"

#: Default setting for validating system metadata when retrieved.  Note that
#: validating every sysmeta instance will likely be kind of slow, especially
#: is a cache is not provided to the client.
VALIDATE_SYSTEM_METADATA = False

#: These HTTP response status codes are OK.
HTTP_STATUS_OK = [200, 301, 302]

#: Default cache to use with client connections.  Setting to None prevents 
#: caching of any responses.  Setting to "/tmp" will cache responses in
#: the /tmp filesystem
HTTP_RESPONSE_CACHE = None
