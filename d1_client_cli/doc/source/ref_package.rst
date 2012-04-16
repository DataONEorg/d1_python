Package
-------

Commands that relate to the creation and manipulation of data packages.


.. _create:

create [:term:`package-id <pid>` [:term:`scimeta <pid>` [:term:`scidata <pid>` ...]]]
`````````````````````````````````````````````````````````````````````````````````````
Create a new package, optionally supplying the the :term:`pid` of this package, the :term:`Science Metadata Object <Science Metadata>`, and a list of :term:`Science Data Objects <Science Data Object>`.

.. _clear:

clear
`````
Clear the current package from memory.

.. _describe:

describe [ scimeta | scidata [:term:`pid`]]
```````````````````````````````````````````
Describe the individual parts of the package without displaying the full content.

.. _help:

help [sub-command]
``````````````````
Help on package commands.

.. _leave:

leave
`````
If in package mode, go back to the base mode.

.. _load:

load [<:term:`pid`>]
````````````````````
Load a package.  If no pid is given, use the current pid.

.. _name:

name <:term:`pid`>
``````````````````
Assign a pid to the package.

.. _save:

save
````
Push the package out to DataONE.

.. _scidata:

scidata
```````
Manipulate the :term:`science data objects<Science Data Object>` in the package.

* **add** Add science data object to the package.
* **del** Remove a given science object from the package.
* **clear**  Remove all science data objects from the package.
* **show** Display the given science object.
* **meta** Display the system meta data for the given science object.
* **desc** Describe the given science object.


.. _scimeta:

scimeta
```````
Manipulate the term:`Science Metadata Object <Science Metadata>` in the package.

* **add** Add the science metadata object to the package.
* **del** Remove the given science metadata object from the package.
* **show** Display the given science metadata object.
* **meta** Display the system meta data for the given science metadata object.
* **desc** Describe the given science metadata object.

Create a new package, optionally supplying the the :term:`pid` of this package, the term:`Science Data Object <Science Data Object>`, and a list of term:`Science Metadata Objects <Science Metadata>`.

.. _show:

show
````
Display the package contents.

