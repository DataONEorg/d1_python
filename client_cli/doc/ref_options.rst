.. _command_line_options:

Overview of command line options
================================

::

  Usage: dataone.py [command] ...

  Options:
    --algorithm=ALGORITHM
                          Checksum algorithm used for a Science Data Object.
    --anonymous           Ignore any installed certificates and connect
                          anonymously
    --no-anonymous        Use the installed certificates and do not connect
                          anonymously
    --authoritative-mn=MN-URI
                          Authoritative Member Node for generating System
                          Metadata.
    --cert-file=FILE      Path to client certificate
    --count=COUNT         Maximum number of items to display
    --cn-url=URI          URI to use for the Coordinating Node
    --from-date=DATE      Start time used by operations that accept a date range
    --key-file=FILE       File of client private key (not required if key is in
                          cert-file
    --mn-url=URI          Member Node URL
    --format-id=OBJECT-FORMAT
                          ID for the Object Format to use when generating System
                          Metadata
    --formatId=OBJECT-FORMAT
                          ID for the Object Format to use when generating System
                          Metadata
    --origin-mn=MN-URI    Originating Member Node to use when generating System
                          Metadata
    --query=QUERY         Query string (SOLR or Lucene query syntax) for
                          searches
    --rights-holder=SUBJECT
                          Subject of the rights holder to use when generating
                          System Metadata
    --search-format-id=OBJECT-FORMAT
                          Include only objects of this format when searching
    --start=START         First item to display for operations that display a
                          list_objects of items
    --submitter=SUBJECT   Subject of the submitter to use when generating System
                          Metadata
    --to-date=DATE        End time used by operations that accept a date range
    -v, --verbose         Display more information
    --no-verbose          Display less information
    --editor              Editor to use for editing operation queue
    --no-editor           Use editor specified in EDITOR environment variable
    --allow-replication   Allow objects to be replicated.
    --disallow-replication
                          Do not allow objects to be replicated.
    --replicas=#replicas  Set the preferred number of replicas.
    --add_blocked=MN      Add blocked Member Node to access policy.
    --add_preferred=MN    Add Member Node to list_objects of preferred
                          replication targets.
    --cn=HOST             Name of the host to use for the Coordinating Node
    --mn=HOST             Name of the host to use for the Member Node
    -i, --interactive     Allow interactive commands
    --no-interactive      Don't allow interactive commands
    -q, --quiet           Display less information
    --debug               Print full stack trace and exit on errors
    -h, --help            show this help message and exit
