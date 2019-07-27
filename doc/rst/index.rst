DataONE Python Products
===========================

DataONE provides a number of products implemented in Python and Java, as part of the :term:`Investigator Toolkit (ITK)`. Potential users of these products include software developers, Member Node partners and end users. Only the Python products are outlined in this document.

For software developers, DataONE provides development libraries implemented in Python. These provide functionality commonly needed by projects that interact with the DataONE infrastructure. It is recommended that applications implemented in Python use the libraries instead of interacting directly with the infrastructure as this is likely to reduce the development effort.

For Member Node partners, DataONE provides a Member Node (MN) implemented in Python, called Generic Member Node (GMN).

Lastly, DataONE provides various tools intended for end users, also implemented in Python. These include ONEDrive and the DataONE Command Line Client.


Contents
~~~~~~~~

.. toctree::
  :maxdepth: 1

  d1_util/index
  d1_onedrive/index
  d1_cli/index

  d1_gmn/index

  d1_common/index
  d1_client/index

  d1_scimeta/index
  d1_test/index
  d1_dev/index

  d1_csw/index


Utilities (for end users)
~~~~~~~~~~~~~~~~~~~~~~~~~

Command Line Utilities and Examples
```````````````````````````````````

.. include:: ./d1_util/overview.rst

\

ONEDrive
````````

.. include:: ./d1_onedrive/overview.rst

\

Command Line Interface
``````````````````````

.. include:: ./d1_cli/overview.rst

\

Generic Member Node (GMN)
`````````````````````````

.. include:: ./d1_gmn/overview.rst

\

Python Libraries (for software developers)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Common Library
``````````````

.. include:: ./d1_common/overview.rst

\

Client Library
``````````````

.. include:: ./d1_client/overview.rst

\

Science Metadata Validator
``````````````````````````

.. include:: ./d1_scimeta/overview.rst

\

Test Utilities
``````````````

.. include:: ./d1_test/overview.rst

\

Development Tools
`````````````````

.. include:: ./d1_dev/overview.rst

\

CSW Harvester
`````````````

.. include:: ./d1_csw/overview.rst
