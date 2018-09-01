ONEDrive Mockups
================

For reference, these alternatives were considered for how ONEDrive should be implemented.

The initial implementation of ONEDrive was a simple proof of concept that enabled access to objects on a specific Member Node.

The second implementation was based on the ``standalone`` mockup below and allowed the user to perform searches by manipulating the filesystem path. Instead of representing a folder hierarchy, the path was used for specifying a faceted search. This system proved to be too complex to use. It also caused the filesystem to be virtually infinitely recursive, which caused problems for file managers and filesystem searches.

The third implementation was based on the ``onemercury-integration`` and implemented the concept of a DataONE Workspace.

The fourth implementation replaced the DataONE Workspace concept with the Zotero citation manager.

Contents:

.. toctree::
  :maxdepth: 1

  overview-of-mockups
  native-integration/index
  onemercury-integration/index
  standalone/index
