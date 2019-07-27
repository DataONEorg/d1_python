GMN Management Commands
=======================

.. toctree::
  :hidden:

  commands_generated.rst

GMN Commands are commands that are started from the command line on
the GMN server via ``manage.py``. E.g.,

.. highlight: bash

::

    $ manage.py audit-proxy-sciobj --pid-path /tmp/objects.txt

- The commands provide functionality for maintaining and administrating a GMN instance as described in this section. The information below is also available from the commands themselves by starting them with the ``--help`` switch.

- The GMN service does not have to be running in order for the commands to work, so the commands can be used for performing maintenance and repair tasks on a server that is down, or where the Apache web server (which is used for hosting GMN) is not yet installed.

.. include:: commands_generated.rst
