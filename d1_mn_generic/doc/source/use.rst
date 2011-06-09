Using GMN
=========




GMN is an implementation of a :term:`MN`. It provides an implementation
of all MN APIs. GMN can be used as a as a workbone or as a reference for a
3rd party MN implementation. GMN can also be used as an "adapter", making it
possible for a 3rd party system to become a MN and expose its objects to
DataONE with a minimum of effort. In this mode, we refer to GMN as the
adapter and the 3rd party system as the adaptee.

When used as an adapter, GMN provides a minimal REST API that the adaptee
can call into to expose its objects, in a process we refer to as object
registration. After registration, GMN exposes objects on behalf of the
:term:`adaptee`.



#.
  The adaptee calls into GMN with a REST call for each object that it wants to
  expose through DataONE. Each REST call provides GMN with either a full SciMeta
  or SciData object (in standalone mode) or URL to such an object (in adapter
  mode), and a corresponding SysMeta object.

#.
  GMN will then serve collection related calls directly from its database.

#.
  When the bytes of a SciData or SciMeta object are requested, GMN serves the
  object from local storage in standalone mode or uses the URL stored in its
  database to retrieve the object from the adaptee's storage facilities and
  streams it out, acting as a streaming proxy in adapter mode.
