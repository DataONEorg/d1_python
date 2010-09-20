'''
Module d1pythonitk.const
========================

:Created: 20100111
:Author: vieglais

Provides various constants for the python DataONE client.

Note that many of these parameters should be retrieved from the root node of D1
'''
import d1pythonitk

#: :const: Version of this software
VERSION = d1pythonitk.__version__

#: types of objects in the DataONE system
#: These need to be replaced with URIs, and should be discoverable from the
#: Coordinating Node introspection data
OBJECT_CLASSES = ['data', 'metadata', 'system']

#: Maximum number of entries per list objects request
#: TODO: Retrieve this from the CN introspection
MAX_LISTOBJECTS = 1000

#: Default number of objects to retrieve in a list objects request
DEFAULT_LISTOBJECTS = 100

#: HTTP Response timeout in seconds, float.
#: TODO: retrieve this from D1 root
RESPONSE_TIMEOUT = 30.0

#: HTTP User Agent that this software is known as
USER_AGENT = 'pyd1/%s +http://dataone.org/' % VERSION

#: The root of all DataONE.  Used to perform introspection on the system when
#: no other node information is provided.
URL_DATAONE_ROOT = 'http://cn-dev.dataone.org/cn/' # "http://cn.dataone.org/"

#: Path to append to target base for the object collection
#: TODO: retrieve this from D1 root
URL_OBJECT_LIST_PATH = 'object'

#: Path to append to target base for a specific object
#: TODO: retrieve this from D1 root
URL_OBJECT_PATH = 'object/'

#: Path to append to target base for system metadata collection
#: TODO: retrieve this from D1 root
URL_SYSMETA_PATH = 'meta/'

#: Path to append to target base for the access log collection.
#: TODO: retrieve this from D1 root
URL_ACCESS_LOG_PATH = 'log'

#: Path to append to target base for the monitor object collection.
URL_MONITOR_OBJECT_PATH = 'monitor/object'

#: Path to append to target base for the resolve call.
URL_RESOLVE_PATH = 'resolve/'

#: Path to append to target base for the node call.
URL_NODE_PATH = 'node/'

#: Path to the DataONE system metadata schema
#: TODO: retrieve this from D1 root
SYSTEM_METADATA_SCHEMA_URL = "https://repository.dataone.org/software/cicore/"+\
                             "trunk/schemas/systemmetadata.xsd"

# Path to the DataONE ObjectList schema.
OBJECTLIST_SCHEMA_URL = "https://repository.dataone.org/software/cicore/"+\
                             "trunk/schemas/objectlist.xsd"

# Path to the DataONE MonitorObject schema.
MONITOR_OBJECT_SCHEMA_URL = "https://repository.dataone.org/software/cicore/"+\
                             "trunk/schemas/monitor_object.xsd"

#: These HTTP response status codes are OK.
HTTP_STATUS_OK = [200, 300, 301, 302, 303, 307]

#: Default cache to use with client connections.  Setting to None prevents 
#: caching of any responses.  Setting to "/tmp" will cache responses in
#: the /tmp filesystem
HTTP_RESPONSE_CACHE = None
