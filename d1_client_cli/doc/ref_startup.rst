Startup
=======

When the CLI is started, it attempts to load the :ref:`session` variables from
a default configuration file named ``.dataone_cli.conf``, located in the user's
home directory. If the configuration file is not present, the session variables
are set to default values as shown in the ``Default`` column in the
:ref:`overview of session variables <session_variables>`.

The CLI then applies any options and executes any commands specified on the
:ref:`command line <Command line arguments>`, in the specified order. This
includes any :ref:`set <set>` commands that modify the session variables.


.. _command_line_arguments:

Command line arguments
~~~~~~~~~~~~~~~~~~~~~~

The CLI accepts a set of options and arguments on the command line. The options
are used for setting the session variables. The arguments are executed as CLI
commands. By default, the CLI will enter interactive mode after modifying the
session according to the options and executing any commands provided as
arguments. This can be prevented by passing the :ref:`--no-interactive` option
or giving the :ref:`exit` command as the last argument. When the CLI enters
interactive mode, the session that was set up with command line options remains
active.

The command line arguments can also include commands that alter the session.
E.g., the following examples are equivalent. Each will load the session from the
user's ``~/.dataone_cli.conf`` file, download the ``mypid`` object from
``mymembernode``, store it in ``myfile`` and exit.

::

  $ dataone --no-interactive --mn-url http://mymembernode.org/mn 'get mypid myfile'

::

  $ dataone --no-interactive 'set mn-url http://mymembernode.org/mn' 'get mypid myfile'

::

  $ dataone 'set mn-url http://mymembernode.org/mn' 'get mypid myfile' exit


Commands that contain spaces or other symbols that have special meaning to the
shell must be quoted. The examples use single quotes. Double quotes can also be
used if it's desired to have the shell expand variables.

Since any CLI command is accepted on the command line, sessions can also be
loaded with the :ref:`load` command. If the CLI is called from a script, it
may be desirable to start with a known, default session. This can be
accomplished by issuing the :ref:`reset` command before any other commands.

When the session variables are set with the options, they are all applied
before any of the commands specified as arguments are executed. When the session
variables are specified with arguments, such as :ref:`set`, they become
active when they are specified and only apply to arguments specified later on
the command line.

Also see :ref:`command_line_options`.
