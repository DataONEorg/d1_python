Architecture
============

.. graphviz::

  digraph G {
    size = "8,20";
    ratio = "compress";
    "Linux / OSX" -> "FUSE Driver" -> "FUSE for Python" -> "ONEDrive";
    "Windows" -> "Dokan Driver" -> "Dokan for Python" -> "ONEDrive";
    "DataONE Client Library\n(Python)" -> "ONEDrive";
    "DataONE Common\n(Python)" -> "ONEDrive";
    "SolR Client\n(Python)" -> "ONEDrive";
    libzotero -> ONEDrive;
  }


Resolvers
---------

The resolvers are classes that "resolve" filesystem paths to lists of files and
folders for those paths. The resolvers are arranged into a hierarchy. Each
resolver examines the path and may resolve the path itself or pass control
to another resolver.

Resolvers deeper in the hierarchy corresponds to sections that are further to
the right in the path. If a resolver passes control to another resolver, it
first removes the section of the left side of the path that it processed. Thus,
each resolver needs to know only how to parse the section of the path that it is
designed to handle. This also enables the same functionality to be exposed
several places in the filesystem. For instance, the resolver for the object
package level can be reached though each of the root level search types.

If a resolver determines that the path that it has received is invalid, it can
abort processing of the path by raising a PathException.


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
      "FlatSpace";
      "ObjectTree";
    }
    {
      rank = same;
      "Author";
      "Region";
      "Single";
      "Taxa";
      "Time Period";
    }
    {
      rank = same;
      "Resource Map";
    }
    {
      rank = same;
      "DataONE Object";
    }

    Root -> "FlatSpace";
    Root -> "ObjectTree";

    "ObjectTree" -> "Author";
    "ObjectTree" -> "Region";
    "ObjectTree" -> "Single";
    "ObjectTree" -> "Taxa";
    "ObjectTree" -> "Time Period";

    "FlatSpace" -> "Resource Map";

    "Author" -> "Resource Map";
    "Region" -> "Resource Map";
    "Single" -> "Resource Map";
    "Taxa" -> "Resource Map";
    "Time Period" -> "Resource Map";

    "Resource Map" -> "DataONE Object"
  }

- The resolvers are all derived from the ``Resolver`` class, not from each
  other.

- Each resolver has three public methods, ``get_attributes()``,
  ``get_directory()`` and ``read_file()``. ``get_attributes()`` returns the
  attributes for a file or folder. ``get_directory()`` returns the directory
  contents for a folder. ``read_file()`` returns sections of a DataONE object.

- The ``Root`` resolver renders the root directory, which contains a set of
  directories designating different types of interactions which can be performed
  with the DataONE infrastructure. It also parses the root elements of paths and
  transfers control to the appropriate path resolver.

- All the resolvers handle paths as lists of path segments. The root resolver
  performs the conversion of the path string to a list of path segments by
  splitting the path on the path separator and unescaping the segments. This
  allows the path segments to contain DataONE identifiers that include the path
  separator and simplifies path handling in the resolvers.

- ``ObjectTree`` ObjectTree renders a filesystem folder structure that
  corresponds with the hierarchy of collections in the Zotero library. It takes
  a source tree generator as input and that generator is currently the Zotero
  client. This abstraction makes it easy to support additional online libraries,
  sky drives and reference managers in the future.

- ``FlatSpace`` enables direct access to objects and enables users to share
  short ONEDrive paths to directly access specific objects.

- ``Resource Map`` renders the contents of a OAI-ORE Resource Map.

- ``DataONE Object`` renders the folder view of a single DataONE object.


The Root resolver
`````````````````

As an example of the pattern that the resolvers follow, consider the Root
resolver. The Root resolver is responsible for rendering the root directory,
``/``, and for dispatching paths out to the other resolvers. Only the root
folder is handled by the Root resolver.

``get_attributes("/")``: Return the attributes for ``/`` (0 size, directory).

``get_attributes("/ObjectTree")``: Not handled by the Root resolver. The Root
resolver strips off ``/ObjectTree``, and passes the remaining path, ``/`` to the
ObjectTree resolver. So, even though ``/ObjectTree`` is returned by
``get_directory("/")`` (see below) of the Root resolver, that same path is not
handled by the Root resolver.

``get_attributes("/ObjectTree/some/other/path")``: Same as
``get_attributes("/ObjectTree")``, except that the path passed to the
ObjectTree resolver is now ``/some/other/path``.

``get_attributes("/invalid")``: This invalid path is handled by the Root
resolver, which raises an InvalidPath exception.

``get_directory("/")``: Return directories for all of the valid 1st level
resolvers, such as ObjectTree.

``get_directory("/ObjectTree")``: Not handled by the Root resolver. As with
the equivalent ``get_attributes()`` call, the path is actually the root for the
ObjectTree resolver.

``get_directory("/ObjectTree/some/other/path")``: Same as
``get_directory("/ObjectTree")``, except that the path passed to the
ObjectTree is now ``/some/other/path``.


Path representation
-------------------

Only the driver specific part of ONEDrive handles paths as strings. The bulk
of the code handles paths as lists of path elements. The elements are strings
or Unicode. They do not contain any escaped characters. The elements may contain
characters that have special meaning in the filesystem, such as the path
separator character ("/" on \\*nix). If so, these characters do NOT have the
special meaning that they would have in a normal path string. When joining
the segments together to a path string, the special characters would be
escaped.

Normally, when splitting the root path, "/", one ends up with a list of two
empty strings. The first empty string shows that the path is absolute (starting
at root), and the second that there is nothing after root. In ONEDrive, all
paths represented as lists of path segments are assumed to be rooted, so the
first, empty, element is removed.


Callbacks
---------

The FUSE callbacks and how these are handled.


getattr()
`````````

``getattr()`` gets called on any path that the user attempts to access and any
path that has previously been returned by ``readdir()``. ``getattr()`` returns
information, such as size, date and type, for a single item. In ONEDrive, the
type of an item is either a file or a folder.

ONEDrive handles ``getattr()`` calls as follows:

#. The keys in the attribute cache are searched for a match to the path. If a
   match is found, the attributes for the file or folder are returned.

#. If the path was not found in the cache, ``get_attributes()`` is called in the
   root resolver.

#. ``getattr()`` caches the result, then returns it.


readdir()
`````````

``readdir()`` is only called for folders. It returns the names of items in a
folder. It does not return any other information, such as the type of the item.
FUSE calls ``getattr()`` for each of the items returned by ``readdir()`` to get
their type, size and other information.

FUSE assumes that the root, "/", is a folder, so ``getattr()`` is not called for
the root before ``readdir()`` is called on the root. This is the only exception
to the general pattern of interactions between `getattr()` and `readdir()`.

By calling ``getattr()`` and ``readdir()`` in a cyclic pattern, FUSE recursively
discovers the folder tree in the filesystem, the contents of the folders, and
the sizes of both files and folders.

FUSE only calls ``readdir()`` on folders that were previously designated as
folders and valid paths by ``getattr()``.

ONEDrive handles ``readdir()`` calls as follows:

#. The keys in the directory cache (see `readdir()`_) are searched for a match
   to the path. If a match is found, the names of the contents for the folder
   are returned.

#. ``readdir()`` caches the result in the directory cache and returns it to
   FUSE.


Debugging
---------

When first mounting ONEDrive, the filesystem will be hit with various automated
requests in order for the OS to learn about the filesystem. This causes trouble
when debugging. On Ubuntu, the automated requests can be disabled temporarily by
killing the gvfs processes::

  $ sudo pkill -9 -f gvfs


Future improvements
-------------------

There's a lot more that can be done with Zotero integration if desired. For
instance, ONEDrive could enable access to other information that can be stored
in Zotero libraries, such as tags, notes and attached objects.

ONEDrive could detect updates in Zotoro while it is running and dynamically
update itself. Currently, ONEDrive only refreshes its caches during startup.


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
