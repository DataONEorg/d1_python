Select the DataONE Tier
=======================

DataONE has defined several tiers, each of which designates a certain level of
functionality exposed by the Member Node. The tiers enable Member Nodes to
implement only the functionality for the level at which they wish to participate
in the DataONE infrastructure.

The tiers are as follows:

======= ========================================================================
Tier 1  Read, public objects
Tier 2  Access controlled objects (authentication and authorization)
Tier 3  Write (create, update and delete objects)
Tier 4  Replication target
======= ========================================================================

Each tier implicitly includes all lower numbered tiers. For instance, a Tier 3
node must implement tiers 1, 2 and 3.

GMN supports all tiers. To select the tier for your Member Node, take the
following into account:

* A Tier 1 node is typically used for exposing existing data to DataONE. As
  there is no support for manipulating the data through DataONE interfaces in
  this tier, GMN cannot be populated with objects while in this tier. Therefore,
  GMN should not initially be set to this tier. Instead, set GMN to Tier 3,
  populate the node with objects, and then set the Tier to 1.

* A Tier 2 node allows the access to objects to be controlled via access control
  lists (ACLs). Using this Tier implies the same strategy as for Tier 1.

* A Tier 3 node allows using DataONE interfaces to set up the objects on the
  Member Node, for instance by using the DataONE Command Line Interface or by
  creating Python scripts or Java programs that are based on the libraries
  provided by DataONE. The objects can be set up with storage managed either by
  GMN itself or by another, independent server that makes the object data
  available on the web. Access to the write functions is restricted by a
  whitelist.

* A Tier 4 member node can act as a replication target, which allows the Member
  Node operator to provide storage space to DataONE (for storing object
  replicas).

When you have determined which tier to use, edit ``settings_site.py``::

  $ sudo pico /var/local/dataone/gmn/lib/python2.6/site-packages/service/settings_site.py

* Set TIER to 1, 2, 3 or 4.
