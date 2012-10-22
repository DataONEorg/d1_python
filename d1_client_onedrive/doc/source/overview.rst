ONEDrive is part of the DataONE :term:`Investigator Toolkit (ITK)`. It enables
the DataONE infrastructure to be mounted and accessed like a regular filesystem
on Windows, Linux and OS X systems.

.. graphviz::

  digraph G {
    size = "6,20";
    ratio = "compress";
    "Linux / OSX" -> "FUSE Driver" -> "FUSE for Python" -> "ONEDrive";
    "Windows" -> "Dokan Driver" -> "Dokan for Python" -> "ONEDrive";
    "DataONE Client Library\n(Python)" -> "ONEDrive";
    "DataONE Common\n(Python)" -> "ONEDrive";
    "SolR Client\n(Python)" -> "ONEDrive";
  }
