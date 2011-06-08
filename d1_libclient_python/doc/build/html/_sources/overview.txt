Overview
========

:d1baseclient:
  Implements DataONEBaseClient, which extends restclient.RESTClient with DataONE
  specific functionality common to CN and MN clients.

:mnclient:
  Implements MemberNodeClient, which extends d1baseclient.DataONEBaseClient
  with MN specific functionality.

:cnclient:
  Implements CoordinatingNodeClient, which extends
  d1baseclient.DataONEBaseClient with CN specific functionality.

:d1client:
  Implements:
  - DataONEClient, which uses cn- and mn clients to perform high level operations
  against the DataONE infrastructure.
  - DataONEObject, which wraps a single object and adds functionality such as
  resolve and get.

:solrclient:
  Functionality for working with the Solr index behind Mercury. Will probably be
  moved into d1common. Ignore for now.

:logrecorditerator:
  Implements an iterator that iterates over the entire set of LogRecords 
  for a DataONE node. Data is retrieved from the target only when required.
  
