Create and Consume OAI-ORE Documents
====================================

d1_pyore is a DataONE python library for working with `OAI-ORE`_ documents which 
are used by DataONE Member Nodes to describe data packages.

Two commandline scripts ``ore2txt`` and ``pids2ore`` are included to produce a
more human readable representation of an OAI-ORE document and to create an OAI-ORE 
document from a list of identifiers respectively.

A brief tutorial_ is provided.

Dependencies
------------

  * rdflib_ >= 4.0
  * `rdflib-jsonld`_
  * requests_


.. _OAI-ORE: https://www.openarchives.org/ore/
.. _rdflib: https://github.com/RDFLib/rdflib
.. _rdflib-jsonld: https://github.com/RDFLib/rdflib-jsonld
.. _requests: http://docs.python-requests.org/en/master/
.. _tutorial: tutorial.ipynb

