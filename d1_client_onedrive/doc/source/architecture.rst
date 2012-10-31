Architecture
============

Production
----------

The main components of ONEDrive when in regular operation.

.. graphviz::

  digraph G {
    ranksep = .75;
    size = "7,20";
    dpi = 72;
    node [shape = box];
    "ONEDrive" -> "FUSE Callbacks"
    "ONEDrive" -> "Dependency Checker"
    "FUSE Driver" -> "FUSE Callbacks"
    "FUSE Callbacks" -> Cache
    "FUSE Callbacks" -> Resolvers
    "Utility Classes" -> Resolvers
    "Resolvers" -> "Command Processor"
    "Command Processor" -> "Solr Client"
    "Command Processor" -> "DataONE Client"
  }

  /*
      subgraph cluster0 {
        node [style=filled, color=white];
        style=filled;
        color=lightgrey;
        label = "Utility Classes";
        "Directory"
        "FacetPathParser"
        "Filename Extensions"
        "PathException"
        "QueryEngineDescription"
        "Resolver ABC"
        "Settings"
      }
  */

The utility classes include ``Directory``, ``FacetPathParser``,
``PathException``, ``Filename Extensions``, ``QueryEngineDescription``,
``ResolverABC``, ``Settings``.



Testing and Debugging
---------------------

The main components of ONEDrive when testing and debugging.

.. graphviz::

  digraph G {
    ranksep = .75;
    size = "7,20";
    dpi = 72;
    node [shape = box];
    "Unit Tests" -> Resolvers
    "Unit Tests" -> "Utility Classes"
    "Resolvers" -> "Command Echoer"
  }

When testing and debugging, the FUSE specific classes are replaced by the unit
testing framework. Also, `Command Processor`_ is replaced with ``Command
Echoer``, a component that simply echoes the commands back instead of returning
actual results. The unit tests for the resolvers compare the echoed commands
with the commands that were expected to be issued for a given path.

One consequence of this is that the FUSE related classes and the ``Command
Processor`` are not tested. There is almost no code in the FUSE related classes
and what is there is linear in nature and is fully tested for each time the
drive is mounted and a path is opened. The ``Command Processor`` contains more
logic but is hard to test reliably since it interacts with databases that change
over time.

This layout facilitates TDD, as the unit tests can be run quickly, with
reproducible results.


Resolvers
---------

The resolvers are classes that "resolve" filesystem paths to lists of files and
folders for those paths. The resolvers are arranged into a hierarchy. Each
resolver examines the path and may resolve the path itself and/or pass control
to another resolver. If a resolver does both, its list of files and folders
appears above the ones provided by resolvers deeper in the hierarchy.

Resolvers deeper in the hierarchy corresponds to sections that are further to
the right in the path. If a resolver passes control to another resolver, it
first removes the section of the left side of the path that it processed. Thus,
each resolver needs to know only how to parse the section of the path that it is
designed to handle. This also enables the same functionality to be exposed
several places in the filesystem. For instance, the resolver for the object
package level can be reached though each of the root level search types.

If a resolver determines that the path that it has received is invalid, it can
abort processing of the path by raising a PathException. The resolver stores a
brief error message in the exception. The exception is caught by the Root
resolver, which renders it as a file in the ONEDrive filesystem, using the
error message as the filename.


The hierarchy of resolvers
``````````````````````````

.. graphviz::

  digraph G {
    ranksep = .75;
    size = "7,20";
    dpi = 72;
    node [shape = box];
    {
      rank = same;
      Root;
    }
    {
      rank = same;
      "Preconfigured Search";
    }
    {
      rank = same;
      "Faceted Search Selector";
      "Flat Space";
      Status;
    }
    {
      rank = same;
      "Faceted Search";
    }
    {
      rank = same;
      "DataONE Object";
    }
    {
      rank = same;
      Package;
    }
    {
      rank = same;
      "Science Object";
    }

    Root -> "Faceted Search Selector";
    Root -> "Preconfigured Search";
    Root -> "Flat Space";
    Root -> Status

    "Faceted Search Selector" -> "DataONE Object";
    "Faceted Search Selector" -> "Faceted Search";
    "Preconfigured Search" -> "Faceted Search Selector"
    "Flat Space" -> "DataONE Object";
    Status -> "Coordinating Nodes";
    Status -> "Member Nodes";

    "Faceted Search" -> "DataONE Object";

    "DataONE Object" -> Package
    "DataONE Object" -> "Science Object"

    Package -> "Science Object"
    Package -> "System Metadata"

    "Science Object" -> "System Metadata"
    "Science Object" -> "Science Metadata"
    "Science Object" -> "Science Data"
  }

Notes
`````

- The resolvers are all derived from ``ResolverABC``, not from each other.

- The ``Root`` resolver renders the root directory, which contains a set of
  directories designating different types of interactions which can be performed
  with the DataONE infrastructure. It also parses the root elements of paths and
  transfers control to the appropriate path resolver.
  
- All the resolvers handle paths as lists of path segments. The root resolver performs
  the conversion of the path string to a list of path segments by splitting
  the path on the path separator and unescaping the segments. This allows the
  path segments to contain DataONE identifiers that include the path separator
  and simplifies path handling in the resolvers.

- The ``Faceted Search Selector`` exists so that faceted search can be turned off
  once a specific object has been selected. In other words, the path::

    /FacetedSearch/@facet1/#value1/@facet2/#value2/mydataonepid/science_object.jpg

  does not cause a faceted search to be performed even though one is included.
  The user has already found and selected an object, so the ``Faceted Search
  Selector`` just strips the faceted search section off the path and passes
  control to ``Package``. This eliminates superfluous searches. It also causes the
  path to remain valid even if the specified object stops matching the facets in
  the future.

- ``Faceted Search`` also appears under ``Preconfigured Search``. This enables the
  user to specify preconfigured searches for various classes of objects of
  interest while still enabling the user to use faceted search to further narrow
  down the results from the preconfigured searches.

- ``Flat Space`` enables direct access to objects and enables users to share
  short ONEDrive paths to directly access specific objects.

- ``DataONE Object`` determines what type of object has been selected and calls
  a resolver that is appropriate for the type. Currently, regular science
  objects and packages are supported.

- ``Package`` renders the contents of a OAI-ORE Resource Map.

- The ``Status`` hierarchy is not implemented. It's just an indication of how
  other DataONE related information can be exposed in the filesystem.


Command processor
-----------------

To retrieve lists of files and folders for display in the filesystem, the
resolvers issue commands to the Command processor. The Command processor
transforms the commands into one or more queries against the DataONE Solr index
and the DataONE infrastructure and wraps up the results.


Path representation
-------------------

Only the driver specific part of ONEDrive handles paths as strings. The bulk
of the code handles paths as lists of path segments. The segments are strings
or Unicode. They do not contain any escaped characters. The segments may contain
characters that have special meaning in the filesystem, such as the path
separator character ("/" on *nix). If so, these characters do NOT have the
special meaning that they would have in a normal path string. When joining
the segments together to a path string, the special characters would be
escaped.

Normally, when
splitting the root path, "/", one ends up with a list
of two empty strings. The first empty string shows that the path is absolute
(starting at root), and the second that there is nothing after root. In ONEDrive,
all paths represented as lists of path segments are assumed to be rooted, so
the first, empty, segment is removed. 



Index
-----

.. toctree::
  :numbered:
  :maxdepth: 2

  setup

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
