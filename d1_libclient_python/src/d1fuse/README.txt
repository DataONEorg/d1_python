README for d1fuse
=================

FUSE is Filesystem in User Space, and d1fuse implements a FUSE_ interface to
DataONE, so that the DataONE infrastructure can be mounted and accessed like
a regular filesystem on Linux and OS X systems.

Status: Pre-alpha, design phase really.  Proof of concept, that sort of thing.


Design Notes
------------

Start off with a really inefficient, network intensive design with no / minimal
caching.

Currently just hits on a single member node, and only retrieves the fist 10
objects.

The basic model being used is /<collection>/<object>

Could do something like this for multiple nodes::

  + nodes
    + node1
      + meta
      + object
      + log
    + node2
    ...


Perhaps::

  + node1
    + content
      + <identifier>
        + sysmeta
        + metadata
        + data
      + <identifier>
      ...
    + log


Would be better to present content as a single unified filesystem view, which
could be supported by the SOLR indexes on the CNs (fast query critical).

Perhaps use facets from the SOLR index to enable drill down into different 
topics.  Plenty of ways to arbitrarily present the content in a file system 
hierarchy view.

Important: Note that FUSE hits file descriptors a lot, so caching is essential 
for any sort of reasonable response.  Also important for nodes to support 
operations like describe(identifer) for efficient retrieval of information 
about objects.


.. FUSE:: http://fuse.sourceforge.net/

.. macfuse:: http://code.google.com/p/macfuse/

.. _fusepy:: http://code.google.com/p/fusepy/
