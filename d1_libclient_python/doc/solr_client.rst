.. _solr_client:

SolrClient
==========

DataONE provides an index of all objects stored in the Member Nodes that form
the DataONE federation. The index is stored in an Apache :term:`Solr` database
and can be queried with the SolrClient.

The DataONE Solr index provides information only about objects for which the
caller has access. When querying the index without authenticating, only records
related to public objects can be retrieved. To authenticate, provide a
certificate signed by :term:`CILogon` when creating the client.


Example
~~~~~~~

::

  # Connect to the DataONE Coordinating Nodes in the default (production) environment.
  c = d1_client.solr_client.SolrConnection()

  search_result = c.search({
    'q': 'id:[* TO *]', # Filter for search
    'rows': 10, # Number of results to return
    'fl': 'formatId', # List of fields to return for each result
  })

  pprint.pprint(search_result)
