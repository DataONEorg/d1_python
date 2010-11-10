Overview
========

GMN is an implementation of a MN. It provides a prototype implementation of all
MN APIs. GMN can be used as a as a workbone or as a reference for a 3rd party MN
implementation. GMN can also be used as an "adapter", making it possible for a
3rd party system to become a MN and expose its objects to DataONE with a minimum
of effort. In this mode, we refer to GMN as the adapter and the 3rd party system
as the adaptee.

When used as an adapter, GMN provides a minimal REST API that the adaptee can
call into to expose its objects, in a process we refer to as object
registration. After registration, GMN exposes objects on behalf of the adaptee.
