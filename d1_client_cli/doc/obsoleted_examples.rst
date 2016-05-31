--------------------------------------------------------------------------------
-- NOTE ------------------------------------------------------------------------
--------------------------------------------------------------------------------

  This use of the CLI has become obsolete and now produces unexpected results.
One the method of scripting becomes defined, this should be revisited.

  This example was removed from source/examples.rst

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------


Using the CLI from scripts
--------------------------

The CLI can be entirely controlled with command line options and can be
prevented from entering interactive mode.

E.g., to download two Science Data Objects from two different :term:`MNs <MN>`,
based on previously prepared session parameters (newlines inserted for
readability)::

  $ ./dataone.py
    'load myparams'
    'set mnurl https://first.mn.com/mn'
    'data pid1 myfile1'
    'set mnurl https://second.mn.com/mn'
    'data pid2 myfile2'
    exit
