Implementation
==============

Dependencies
~~~~~~~~~~~~

.. graphviz::

  digraph G {
    dpi = 60;
    ratio = "compress";
    "DataONE Common" -> CLI
    "DataONE Client Library" -> CLI
  }


Class hierarchy
~~~~~~~~~~~~~~~

.. graphviz::

  digraph G {
    dpi = 60;
    edge [dir="none"]
    ratio = "compress";

    main -> CLI

    CLI -> CommandProcessor
    CLI -> Session

    CommandProcessor -> Session
    CommandProcessor -> OperationMaker
    CommandProcessor -> OperationQueue
    CommandProcessor -> OperationExecuter
    CommandProcessor -> OperationFormatter

    OperationMaker -> Session

    OperationExecuter -> CLICNClient
    OperationExecuter -> CLIMNClient
    OperationExecuter -> PackageCreator
    OperationExecuter -> SystemMetadataCreator

    CLICNClient -> CLIClient
    CLIMNClient -> CLIClient

    Session -> ReplicationPolicy
    Session -> AccessControl
    Session -> SessionVariable

    CLIClient -> "DataONE Client Library"
    "DataONE Client Library" -> "DataONE Common"

    // Move the OperationExecuter to the level below the SessionVariable.
    SessionVariable -> OperationExecuter [style="invis"]
  }

:Command: An action that causes changes only internal to the CLI.

:Operation: An action that causes one or more reads or writes against a DataONE
  Node.

main:
  * Handle command line options.
  * Capture and display internal and external exceptions.

CLI:
  * Generic boiler plate for Python CLI apps.
  * Simple command tokenizing and validation.

CommandProcessor:
  * Manipulate the session.
  * Create, then execute DataONE Read Operations.
  * Create, then queue DataONE Write Operations.
  * Execute queue of DataONE Write Operations.
  * Display the results of DataONE Operations.

OperationMaker:
  * Combine parameters from CommandProcessor and from the session into a DataONE Read or Write Operation.

OperationQueue:
  * Hold a queue of DataONE Write Operations.
  * Edit the queue.
  * Display the queue.

OperationExecuter:
  * Execute a DataONE Read Operation or a queue of Write Operations.


Utility classes
---------------

These are used throughout the main classes and so are kept out of main hierarchy for readability.

.. graphviz::

  digraph G {
    dpi = 60;
    edge [dir="none"]
    ratio = "compress";

    InvalidArguments
    CLIError
    ComplexPath
    MissingSysmetaParameters
  }


Notes
~~~~~

* Read operations are executed immediately.

* Write operations are queued and executed in a batch. The write queue can be
  edited.

* Write operations are decoupled from the session. Each write operation contains
  a copy of the relevant session variables at the time the operation was issued.
  Those variables are then used when the operation is executed.

