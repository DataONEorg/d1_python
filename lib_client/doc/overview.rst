The :doc:`/client/index` works together with the :doc:`/common/index`
to provide functionality commonly needed by client software that connects to DataONE nodes.

The main functionality provided by this library is a complete set of wrappers for all DataONE API methods. There are many details related to interacting with the DataONE API, such as creating MIME multipart messages, encoding parameters into URLs and handling Unicode. The wrappers hide these details, allowing the developer to communicate with nodes by calling native Python methods which take and return native Python objects.

The wrappers also convert any errors received from the nodes into native exceptions, enabling clients to use Python's concise exception handling system to handle errors.
