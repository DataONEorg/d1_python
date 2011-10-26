Setting up the Node registry file.

A Member Node identifies itself by returning a DataONE Node document.

identifier
----------
A unique identifier for the node. This may initially be the same as the baseURL,
however this value should not change for future implementations of the same
node, whereas the baseURL may change in the future. 

name
----
A human readable name of the Node. 

description
-----------
Description of content maintained by this node and any other free style
notes.

baseURL
-------
The URL at which the Node is available.


services
--------
A list of the services available on the Member Node. 

