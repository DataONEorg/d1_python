.. _replication_policy:

Replication Policy
------------------

The Replication Policy contains a list of Member Nodes that are specifically
preferred or blocked as :term:`replication targets <replication target>`. The
Replication Policy also contains a setting that specifies if replication is
allowed or disallowed, and the preferred number of replicas.

The Replication Policy is applied to new objects as they are :ref:`created
<create>`. The Replication Policy can also be updated on existing Science Data
Objects with :ref:`setreplication <setreplication>`.

The DataONE infrastructure will never replicate an object to a Member Node that
is in the list of :ref:`blocked Member Nodes <addblocked>` for that object. If a
Member Node is added to the list of blocked Member Nodes after an object has
been replicated to that Member Node, the DataONE infrastructure will request
that the Member Node in question remove its copy of the object.

If the :ref:`preferred number of replicas <setreplicas>` is larger than the
number of Member Nodes that have been specified as :ref:`preferred replication
targets <addpreferred>`, additional Member Nodes that are not in the blocked
list will automatically be selected as replication targets.

If the preferred number of replicas is modified on an existing Science Data
Object, DataONE will adjust the number of existing replicas by creating and
deleting replicas of that object as needed.

Use the :ref:`get <get>` command without any parameters to view the current
Replication Policy.

Commands to manipulate the Replication Policy:


.. _clearreplication:

clearreplication
````````````````
Clear the replication policy. The cleared replication policy has no
preferred or blocked member nodes, disallows replication and sets the preferred
number of replicas to zero.


.. _addpreferred:

addpreferred <member node>
``````````````````````````
Add Member Node to list of preferred replication targets.


.. _addblocked:

addblocked <member node>
``````````````````````````
Add Member Node to list of blocked replication targets.


.. _remove:

remove <member node>
````````````````````
Remove Member Node from list of preferred or blocked replication targets.


.. _allowreplication:

allowreplication
````````````````
Allow objects to be replicated. 


.. _disallowreplication:

disallowreplication
```````````````````
Disallow replication and set the preferred number of replicas to zero.



.. _setreplicas:

setreplicas <number of replicas>
````````````````````````````````
Set preferred number of replicas. If the preferred number of replicas is set
to zero, replication is also disallowed.
