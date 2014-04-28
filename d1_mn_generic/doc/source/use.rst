Using GMN
=========

After :term:`GMN` has been set up according the setup instructions, it exposes
the complete REST interface that DataONE has defined for Member Nodes.
Currently, the easiest way to interact with GMN is to use the DataONE Command
Line Client (CLI). The CLI is installed automatically with GMN and can be
started by typing "dataone". The CLI can also be scripted to perform tasks such
as bulk object creations to populate an instance of GMN with science data.

See :doc:`setup-local-testing` and the `DataONE Command Line Interface (CLI)
documentation <http://pythonhosted.org/dataone.cli>`_ for more information about
how to use the CLI.

If more comprehensive access to the Node is required, DataONE provides libraries
in Java and Python that simplify the process of interacting with DataONE Member
Nodes and Coordinating Nodes. The libraries can be used as foundations for
custom applications that use the DataONE infrastructure.

.. toctree::
  :maxdepth: 2

  use-general
  use-authn-and-authz
