`DataONE ONEDrive`_ enables the DataONE :term:`Workspace` to be accessed like a
regular filesystem on Windows, Mac OS X and Linux systems. This allows users to
open remote DataONE objects locally and work with them as if they reside on the
user's computer. For instance, a spread sheet that is stored on a Member Node
can be opened directly in Excel.

.. note:: The DataONE Workspace is currently under development and is not yet
  available as a service. Because of this, ONEDrive 2.0 works with a local
  representation of the Workspace, stored in a file called ``workspace.xml``.
  ONEDrive comes with an example ``workspace.xml`` file. To select the DataONE
  objects which should be available in ONEDrive, it is necessary to manually
  edit this file.

.. _`DataONE ONEDrive`: http://pythonhosted.org/dataone.onedrive/
