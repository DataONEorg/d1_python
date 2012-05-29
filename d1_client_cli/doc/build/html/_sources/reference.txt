Reference
=========

.. _session_parameters_intro:

Session parameters
~~~~~~~~~~~~~~~~~~

Various operations can be performed against the :term:`DataONE` infrastructure
via the DataONE Command Line Interface (CLI). The operations obtain the
parameters they require from a set of shared, configurable, values called
:ref:`session parameters <session_parameters>`.


.. _startup:

Startup
~~~~~~~

When the CLI starts, it attempts to load the session parameters from a
configuration file named ``.d1client.conf``, located in the user's home
directory. If the configuration file is not present, the session parameters are
set to default values as shown in the ``Default`` column in the :ref:`overview
of session parameters <session_parameters>`.

The CLI then executes any commands specified on the command line, in the
specified order. This includes any :ref:`set <set>` commands that modify the
session parameters.


.. _command_line_arguments:

Command line arguments
~~~~~~~~~~~~~~~~~~~~~~

One or more commands may be specified on the command line. The CLI will execute
these before entering interactive mode. The CLI can be prevented from entering
interactive mode by adding the :ref:`exit` command to the end of the list of
commands.

E.g., the following command will start the CLI, execute a :ref:`list` command
based on any default values in the ``.d1client.conf`` file and then :ref:`exit`.

::

  $ dataone.py list exit

Commands that contain spaces or other symbols that have specific meaning to the
shell must be quoted with single quotes::

  $ dataone.py 'get mypid myfile'

The session parameters available in interactive mode can be modified on startup
by specifying :ref:`set <set>` commands. E.g., the following is the same as
first running ``dataone.py`` and then typing the two commands, ``set start 100``
and ``set count 10``::

  $ dataone.py 'set start 100' 'set count 10'


.. _commands:

Commands
~~~~~~~~

``<...>`` denotes required arguments.

``[...]`` denotes optional arguments.

``file`` is the filesystem path to a local file.

Commands are case sensitive.


.. toctree::
  :maxdepth: 2

  ref_cli
  ref_session
  ref_access_policy
  ref_replication_policy
  ref_auth
  ref_search
  ref_sci
  ref_package
