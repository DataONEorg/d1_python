.. _access_policy:

Access Policy
-------------

The Access Policy is a list of subjects with associated access levels. The
Access Policy is applied to new objects as they are :ref:`created <create>`. The
Access Policy can also be updated on existing Science Data Objects with
:ref:`setaccess <setaccess>`.

Use the :ref:`get <get>` command without any parameters to view the current
Access Policy.

Commands to manipulate the Access Policy:


.. _allow:

allow <subject> [access level]
``````````````````````````````
Allow access to ``subject``. If ``access level`` is not provided, it defaults to
**read**. Valid access levels are: read, write, changePermission, execute and
replicate. Any access level implicitly includes less permissive levels. E.g.,
giving changePermission to a subject implicitly gives read and write permissions
as well.


.. _deny:

deny <subject>
``````````````
Remove subject from Access Policy.


.. _allowpublic:

allowpublic
```````````
Allow public read.


.. _denypublic:

denypublic
``````````
Deny public read.


.. _denyall:

denyall
```````
Remove all subjects from Access Policy and deny public read. Only the submitter
will have access to the object.



