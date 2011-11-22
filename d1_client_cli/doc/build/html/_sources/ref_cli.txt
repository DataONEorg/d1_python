CLI
---

Commands that relate to the operation of the Command Line Interface itself.


.. _history:

history
```````
Display a list of commands that have been entered.


.. _exit:

exit
````
Exit from the CLI.


.. _help:

help
````
Get help on commands.

``help`` or ``?`` with no arguments displays a list of commands for which help is
available.

``help <command>`` or ``? <command>`` gives help on <command>.


.. _verbose_header:

Verbose
```````
The CLI can be set to display more information as operations are performed by
turning the :ref:`verbose <verbose>` session variable to True.


.. _xml_formatting:

XML formatting
``````````````
Some commands display XML. The CLI can be set to format XML to be more easily
readable by setting :ref:`pretty <pretty>` to True.
